======================================================
MODULE: M10 — Vision, Multimodal & Evaluation
VIDEO: Opening — They See Now
NARRATOR: Prof. Dehghani
DURATION: 4 minutes (~490 words)
======================================================

PART 1: OPENING HOOK
------------------------

I was reviewing engineering drawings last month. Complex CAD diagrams with dozens of components, tolerance annotations, material callouts.

I uploaded one to GPT-4 Vision and asked it to identify potential stress points. It studied the drawing for a few seconds. Then it flagged three areas my team had missed. One was a load-bearing joint where two materials met at a sharp angle. It explained why that geometry could cause fatigue cracking under repeated stress.

That is when I realized -- these models do not just read text anymore. They see.

And if they can see, the range of problems they can solve just expanded by an order of magnitude.

[ANIMATION: Engineering CAD drawing appearing on screen, with AI highlighting three stress points in red, zooming into the critical joint]

PART 2: VISION AND MULTIMODAL AI
------------------------

Vision APIs let you send an image alongside your text prompt. The model processes both together. It can describe what it sees, answer questions about visual content, extract text from photos, analyze charts, interpret diagrams, and compare images.

This is multimodal AI. Not just text in, text out. Text plus images in. Structured answers out.

The technology matured fast. GPT-4 Vision, Gemini's native multimodal input, Claude's vision capabilities -- by 2026, every major model can process images as naturally as they process text. Some can generate images too.

But here is what most people miss. Vision is not just about "what is in this picture." It is about document understanding. A scanned invoice. A handwritten form. A whiteboard photo from a meeting. A screenshot of a dashboard. These are all images that contain structured information, and multimodal models can extract it.

[ANIMATION: Grid of use cases -- CAD drawing, medical scan, invoice, whiteboard photo, dashboard screenshot -- each with an AI extraction arrow showing structured output]

PART 3: REAL-WORLD APPLICATIONS
------------------------

In healthcare, radiologists use vision models as a second pair of eyes on X-rays and MRIs. Not replacing doctors -- augmenting them. Catching anomalies that human fatigue might miss.

In manufacturing, quality control systems photograph every unit on the assembly line. A vision model flags defects in real time. One automotive supplier reported a 34 percent reduction in defective parts after deploying vision-based QC.

In insurance, claims adjusters upload photos of vehicle damage. The model estimates repair costs within seconds. What used to take three days now takes three minutes.

[ANIMATION: Three industry panels -- healthcare (X-ray scan), manufacturing (assembly line QC), insurance (vehicle damage photo) -- each showing AI analysis overlay]

PART 4: THE EVALUATION PROBLEM
------------------------

But here is the hard question. How do you know if any of this actually works? How do you measure whether your AI is accurate, reliable, and safe?

That is evaluation. And it is the most underappreciated skill in AI engineering. Building the model is half the job. Measuring its quality is the other half. This week, you learn both.

PART 5: WHAT YOU WILL BUILD
------------------------

You will send images to vision APIs and build applications that process visual input. Then you will build an evaluation framework -- testing your AI's outputs against ground truth, measuring accuracy, and identifying failure modes.

You are about to give your AI eyes. And then learn how to check its vision.

======================================================
DIGITAL MEDIA NOTES:
- Opening: show a real (anonymized) engineering drawing with AI annotations appearing progressively
- Use case grid: clean, icon-style panels for each industry -- healthcare, manufacturing, insurance
- Evaluation section: introduce the concept with a simple accuracy scorecard graphic
- Consider embedded quiz: "Which is NOT a multimodal input?" (A: Text only / B: Text + Image / C: Text + Audio)
======================================================
