def build_lesson_plan_prompt(topic: str, chapter: str, context: str) -> str:
    return f"""
You are an experienced teacher.

Using ONLY the following textbook content, create a detailed lesson plan.

Topic: {topic}
Chapter: {chapter}

The lesson plan MUST include the following sections clearly labeled:

1. Lesson Title
2. Learning Objectives (3–5 bullet points)
3. Introduction
4. Main Teaching Content
5. Classroom Activities
6. Assessment Method
7. Summary

Rules:
- Base everything strictly on the provided textbook content
- Do NOT add external knowledge
- Use clear, teacher-friendly language
- Do NOT mention the textbook explicitly

TEXTBOOK CONTENT:
{context}

LESSON PLAN:
"""
