======================================================
MODULE: M01 — Getting Started with LLM APIs
VIDEO: TA Basics — API Key Setup and Google Colab
NARRATOR: TA
DURATION: 4 minutes (~400 words)
======================================================

PART 1: WHAT WE ARE SETTING UP
------------------------

Hi everyone. In this video, I will walk you through three things you need before starting the lab: getting your OpenAI API key, setting up Google Colab, and storing your key securely using Colab Secrets.

This should take about five minutes. Follow along step by step, and you will be ready to go.

[ANIMATION: Checklist graphic — three items: 1. OpenAI API Key, 2. Google Colab, 3. Colab Secrets]

PART 2: GETTING YOUR OPENAI API KEY
------------------------

First, go to platform.openai.com. If you do not have an account, create one. You can use your Northeastern email.

Once you are logged in, click on your profile icon in the top right, then select "API keys" from the menu. Click "Create new secret key." Give it a name like "DADS5250" so you remember what it is for.

Important: you will only see this key once. Copy it right now and paste it somewhere safe, like a text file on your desktop. If you lose it, you will need to create a new one.

You will also need to add a payment method under Billing. OpenAI charges per use, but for this course your total cost will likely be under five dollars for the entire semester. You can set a monthly spending limit to be safe. I recommend setting it to ten dollars.

[ANIMATION: Screen recording — navigating platform.openai.com, creating API key, setting billing limit]

PART 3: SETTING UP GOOGLE COLAB
------------------------

Open Google Colab at colab.research.google.com. Sign in with your Google account. We will use Colab for all labs in this course because it runs in the browser and requires no local installation.

Create a new notebook. You should see an empty code cell. That is where we will write our first API call.

PART 4: STORING YOUR KEY IN COLAB SECRETS
------------------------

Never paste your API key directly into a code cell. If you share your notebook or push it to GitHub, anyone can see it and use your key at your expense.

Instead, use Colab Secrets. Click the key icon in the left sidebar. Click "Add a new secret." Name it OPENAI_API_KEY and paste your key as the value. Toggle the "Notebook access" switch to on.

Now in your code, you access it like this:

from google.colab import userdata
api_key = userdata.get("OPENAI_API_KEY")

That is it. Your key stays private. Your notebook stays clean.

[ANIMATION: Screen recording — Colab Secrets panel, adding key, toggling access, showing the two lines of code]

PART 5: COMMON ISSUES
------------------------

A few things that trip people up.

First: "AuthenticationError." This means your key is wrong or expired. Go back to platform.openai.com and check it.

Second: "InsufficientQuotaError." This means you have not added a payment method, or you hit your spending limit. Check your billing page.

Third: "ModuleNotFoundError for openai." Run this in a code cell first: pip install openai. Colab does not always have the latest version pre-installed.

If you run into anything else, post in the discussion board and include the full error message. We will get you sorted out.

Good luck with the lab.

======================================================
DIGITAL MEDIA NOTES:
- Full screen recording walkthrough for Parts 2-4, with mouse cursor highlights and zoom-ins on key buttons
- Show the two-line code snippet for Colab Secrets as an overlay graphic during Part 4
- Common Issues section: consider a three-panel error/solution graphic that students can screenshot for reference
- Add a caption banner: "Never paste API keys directly into code cells"
======================================================
