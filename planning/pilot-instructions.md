# Pilot pack: verify provider access from an affected country

Purpose: before announcing the alternative-provider setup to the class, one
student who is actually in an affected country (China, Iran, or Russia)
spends about 10 minutes confirming the path works from there. This tests the
one thing we cannot test from here: real signup and API reachability.

Send the message below to the pilot student as-is (adjust the greeting).

---

Subject: 10-minute favor: test the course AI setup from your location

Hi <name>,

I am setting up an alternative AI provider for DADS 5250 so that everyone
can run the labs regardless of location, and I need one real-world test from
where you are. It should take about 10 minutes. No VPN please, that is the
point of the test.

Step 1. Create a DeepSeek account at https://platform.deepseek.com
(email or Google sign-in). Note whether signup works and whether you are
able to add a small credit (any payment method you would normally use).

Step 2. Create an API key there (API Keys section).

Step 3. Open this notebook in Google Colab:
https://colab.research.google.com/github/mdehghani86/DADS5250-GenAI/blob/main/labs/M00/M00_Lab0_API_Key_Check.ipynb
In the key sidebar (key icon) add two Secrets, enabling notebook access:
  LLM_PROVIDER = deepseek
  DEEPSEEK_API_KEY = <your key>
Then Run All.

Step 4 (optional, 3 extra minutes). If you can also register at
https://modelstudio.console.alibabacloud.com (Alibaba Model Studio,
Singapore region) and create a key, add it as a third Secret QWEN_API_KEY
and Run All again, so we can confirm the embeddings path too.

Please reply with:
1. Did DeepSeek signup work, and did payment work if you tried it?
2. A screenshot of the "Provider check summary" output from the notebook.
3. Anything that was blocked, slow, or confusing.

Thank you, this directly decides how we roll this out for everyone.

---

## What the outcomes mean

- Both checks PASS: announce to the class using `labs/ALTERNATIVE_PROVIDERS.md`.
- Chat PASSes, embeddings not available: DeepSeek works, Qwen signup is the
  friction; consider the local sentence-transformers fallback for embeddings.
- Signup or API blocked: escalate to the Z.ai option (free GLM models, email
  signup) and re-run this same pilot against it.
