from ollama import ask_llm_change


def group_segments(segments: list, block_sec: int = 120):
    blocks = []
    current = []
    start = segments[0]["start"]

    for s in segments:
        current.append(s)
        if s["end"] - start >= block_sec:
            blocks.append(current)
            current = []
            start = s["end"]

    if current:
        blocks.append(current)

    return blocks


def find_cuts(blocks, min_sec=420, max_sec=1200):
    cuts = []
    start = blocks[0][0]["start"]

    last_block_text = " ".join(s["text"] for s in blocks[0])
    acc_duration = 0

    for i in range(1, len(blocks)):
        block = blocks[i]
        block_text = " ".join(s["text"] for s in block)
        block_duration = block[-1]["end"] - block[0]["start"]
        acc_duration += block_duration

        changed = ask_llm_change(last_block_text, block_text)
        
        if (changed and acc_duration >= min_sec) or acc_duration >= max_sec:
            cuts.append({
                "start": start,
                "end": block[0]["start"]
            })
            start = block[0]["start"]
            acc_duration = 0

        last_block_text = block_text

    cuts.append({
        "start": start,
        "end": blocks[-1][-1]["end"]
    })

    return cuts



import json
with open('./saida.json', 'r') as doc:
    content = doc.read()

data = json.loads(content)
groups = group_segments(data)
custs = find_cuts(groups)
breakpoint()


