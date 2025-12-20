import json
inp = {"dsadsa": "asdasd"}

prompt = """
Task: Segment a long political transcript into thematic cuts.

Rules:
- A cut starts when a new dominant topic clearly begins.
- A cut ends when the dominant topic clearly changes.
- Ignore digressions under 2 minutes.
- Min duration: 8 minutes.
- Max duration: 30 minutes.
- Topics may exceed 30 minutes if they remain coherent; split only if there is a clear internal topic change.
- If a topic is shorter than 8 minutes, merge with the previous cut if thematically coherent.

Topic change indicators:
- Change of main subject or person.
- Change of core political narrative or thesis.
- Clear contextual shift.

Output:
Return ONLY a minified JSON array.
Each item must follow exactly this structure:
{{"start":int,"end":int,"topic":string}}

No explanations.
No markdown.
No extra text.

INPUT:

{0}
""".format([json.dumps(inp, separators=(",", ":"))])


from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.responses.create(
    model="gpt-5-nano",
    input=prompt,
)
