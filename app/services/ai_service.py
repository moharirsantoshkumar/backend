from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_explanation(product, weights):
   prompt = f"""
You are a smart shopping assistant.

Treat rating above 4.5 as excellent, 4.0–4.5 as good, below 4 as average.

User priorities:
- Price: {weights['price']}
- Performance: {weights['performance']}
- Battery: {weights['battery']}
- Rating: {weights['rating']}

Laptop:
Name: {product['name']}
Price: {product['price']}
Processor: {product['processor']}
RAM: {product['ram_gb']} GB
Battery: {product['battery_hours']} hours
Rating: {product['rating']}

Give output in EXACT format:

Pros:
- (max 2 points)
- (max 2 points)

Cons:
- (max 2 points)
- (max 2 points)

Why this fits:
- Give a decisive recommendation in 1–2 lines (e.g., “Best if you prioritize price over battery”)
"""

   response = client.chat.completions.create(
       model="gpt-4o-mini",
       messages=[{"role": "user", "content": prompt}],
       max_tokens=150
   )

   return response.choices[0].message.content.strip()