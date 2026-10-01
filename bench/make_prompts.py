"""Generates bench/prompts.jsonl: 50 prompts (10 per skill x 4 + 10 no-skill)."""
import json

P = {
    "csv-summary": [
        "How many rows are in sales.csv?", "Summarize data/students.csv for me",
        "What columns does orders.csv have?", "Give me stats for the CSV file readings.csv",
        "Show the min and max of each numeric column in temps.csv", "What's in this csv: patients.csv?",
        "Describe the dataset budget.csv", "Count the records in inventory.csv",
        "Average values in the file marks.csv please", "Look at survey.csv and tell me what it contains"],
    "unit-convert": [
        "Convert 12 km to miles", "How many pounds is 70 kg?", "What is 98.6 F in Celsius?",
        "5 gallons is how many litres?", "Convert 300 cm to inches", "How many ounces in 250 grams?",
        "Turn 0 Celsius into Kelvin", "How many feet are in 2 miles?", "Convert 3 cups to millilitres",
        "What is 100 yards in metres?"],
    "note-search": [
        "Find my notes that mention the vaccine fridge", "Search my notes for 'budget meeting'",
        "Which note files talk about Rahul?", "Look up 'deadline' in my notes folder",
        "Do any of my notes mention the clinic schedule?", "Search notes for the word passport",
        "Find where I wrote about the API key rotation", "grep my text notes for 'standup'",
        "What did I write about the hackathon in my notes?", "Search my markdown notes for 'tax'"],
    "pdf-extract": [
        "What does report.pdf say?", "Extract the text from paper.pdf", "Read the first page of invoice.pdf",
        "Give me the content of syllabus.pdf", "What's written in the PDF resume.pdf?",
        "Pull the text out of manual.pdf, first 2 pages", "Summarize lecture1.pdf for me",
        "What is on page 1 of contract.pdf?", "Open brochure.pdf and tell me what it says",
        "Get me the text of thesis.pdf"],
    None: [
        "What is the capital of France?", "Say hello", "Explain recursion in one sentence",
        "What is 2 + 2?", "Tell me a fun fact about octopuses", "Who wrote Hamlet?",
        "Give me three tips for studying", "What does CPU stand for?", "Name a primary colour",
        "What is the speed of light, roughly?"],
}
with open("bench/prompts.jsonl", "w") as f:
    for skill, ps in P.items():
        for p in ps:
            f.write(json.dumps({"prompt": p, "expected": skill}) + "\n")
