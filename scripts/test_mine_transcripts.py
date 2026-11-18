#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""Checks for the token math in mine-transcripts.py. Run: uv run --with pytest pytest scripts/

Stdlib only, so it runs before the project has a test harness.
"""
import base64
import importlib.util
import json
import os
import struct
import tempfile
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("tu", os.path.join(HERE, "mine-transcripts.py"))
tu = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tu)

failures = []


def check(name, got, want):
    if got == want:
        print(f"ok   {name}")
    else:
        print(f"FAIL {name}: got {got}, want {want}")
        failures.append(name)


def write(lines):
    handle = tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8")
    for line in lines:
        handle.write(json.dumps(line) + "\n")
    handle.close()
    return handle.name


def usage_line(request_id, block):
    return {"requestId": request_id,
            "message": {"content": [block],
                        "usage": {"input_tokens": 0, "cache_creation_input_tokens": 100,
                                  "cache_read_input_tokens": 500, "output_tokens": 70}}}


def png(width, height):
    header = b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + struct.pack(">II", width, height)
    return base64.b64encode(header + b"\x00" * 40000).decode()


# An image is sized by its dimensions, never by its base64 payload.
big = png(2976, 4410)
check("payload estimate dwarfs the true size", len(big) // 4 > tu.image_tokens(big) * 5, True)
check("png sized by dimensions", tu.image_tokens(big), int(1058 * 1568 / 750))
check("small png under the cap", tu.image_tokens(png(750, 750)), 750)
check("undecodable image falls back", tu.image_tokens("not-base64!!"), tu.IMAGE_FALLBACK)

# A tool result carrying an image is sized the same way.
block = {"type": "tool_result", "tool_use_id": "t1",
         "content": [{"type": "text", "text": "a" * 400},
                     {"type": "image", "source": {"data": big}}]}
check("result mixes text and image", tu.result_tokens(block), 100 + int(1058 * 1568 / 750))

# Subagent transcripts carry no toolUseResult key; the content block still sizes.
check("string result sizes", tu.result_tokens({"content": "b" * 4000}), 1000)
check("empty result is zero", tu.result_tokens({}), 0)

# A ticket's estimate carries its points and the model and effort it was planned for.
check("estimate reads points and plan",
      tu.estimate("## Estimate\n\n**5 points** — five workflows.\n\n**Opus, medium** — reading."),
      (5, "opus", "medium"))
check("estimate reads a bare number", tu.estimate("## Estimate\n\n**3**\n"), (3, None, None))
check("no estimate", tu.estimate("# A ticket"), (None, None, None))

# A retro entry counts serious findings and the changes asked for after sign-off.
entry = """**Code review**
| Severity | Finding | Outcome | Planning miss |
|---|---|---|---|
| Important | A | Fixed | the ticket |
| Minor | B | Fixed | — |
| Critical | C | Fixed | Tests |

**Changed after sign-off**
- The dialog lists the cooler lots. Planning miss: the wireframe.
- Gray the closing steps.

**Next**
- not counted
"""
check("retro facts", tu.retro_facts(entry), (2, 2))
check("no changes after sign-off", tu.retro_facts("**Changed after sign-off**\n- None.\n"), (0, 0))

# What the owner typed, apart from tool results, skill bodies and harness notes.
check("typed prompt", tu.typed_text({"type": "user", "message": {"content": "no, keep the tick"}}),
      "no, keep the tick")
check("tool result is not typed", tu.typed_text(
    {"type": "user", "message": {"content": [{"type": "tool_result", "content": "x"}]}}), None)
check("skill body is not typed", tu.typed_text(
    {"type": "user", "message": {"content": [{"type": "text", "text": "Base directory for this skill: /a/b"}]}}),
    None)
check("correction caught", bool(tu.CORRECTION.search("No, that's the wrong lot")), True)
check("go-ahead is no correction", bool(tu.CORRECTION.search("yes, go ahead")), False)

# The same command three times running is one retry loop.
check("retry loop", tu.retries(["a", "a", "a", "b", "a", "a", "a", "a"]), 2)
check("model family", tu.family("claude-sonnet-5-5"), "sonnet")

# A redesign drops what a doc said; adding or rewording is not one.
check("addition is no redesign", tu.is_redesign([], ["new rule"]), False)
check("rewording is no redesign", tu.is_redesign(["A day locks at print."], ["A day locks when printed."]), False)
check("replacing is a redesign", tu.is_redesign(["Review holds the cooler step."], ["Complete lists the lots."]), True)
check("rewording one line and appending is no redesign", tu.is_redesign(
    ["A day locks at print."], ["A day locks when printed."] + [f"New rule {i}, with its reason." for i in range(10)]),
    False)
check("slash command is not typed", tu.typed_text(
    {"type": "user", "message": {"content": "<command-name>/clear</command-name>"}}), None)
diff = "+++ b/docs/architecture.md\n@@ -12,2 +12 @@\n-old one\n-old two\n+new\n"
check("hunks read", tu.hunks(diff), [("docs/architecture.md", 12, ["old one", "old two"], ["new"])])
check("heading above a line", tu.heading_at("# Top\n## Cooler\ntext\nmore", 4), "Cooler")
check("owner round trigger", tu.trigger("005-148 — round 3: drop Review's cooler step"), "owner")



def test_every_check_passes():
    assert not failures


if __name__ == "__main__":
    print("\nFAILED" if failures else "\nall passed")
    raise SystemExit(1 if failures else 0)
