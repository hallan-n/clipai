# from transformers import pipeline

# # cria o pipeline de sumarização
# summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# def summarize_segments(transcribe, segments):
#     results = []
#     segs = transcribe["segments"]

#     for (start, end) in segments:
#         # junta os textos que estão dentro do intervalo de tempo
#         text = " ".join(
#             d["text"] for d in segs
#             if start <= d["start"] < end
#         )

#         if not text.strip():
#             continue

#         # evita texto muito longo (máx. 2000 caracteres)
#         input_text = text[:2000]

#         summary = summarizer(
#             input_text,
#             max_length=120,
#             min_length=30,
#             do_sample=False
#         )[0]["summary_text"]

#         results.append({
#             "start": start,
#             "end": end,
#             "summary": summary
#         })

#     return results