======================================================
MODULE: M11 — Workflow Automation & GenAI Platforms
VIDEO: TA Basics — Setting Up n8n
NARRATOR: TA
DURATION: 4 minutes (~420 words)
======================================================

PART 1: WHAT WE ARE SETTING UP
------------------------

Hi everyone. In this video, I will walk you through getting n8n up and running for this week's lab. We will cover three things: creating your n8n account, building your first workflow, and connecting your OpenAI API key.

Follow along step by step and you will be ready for the lab.

[ANIMATION: Checklist graphic -- three items: 1. n8n Account, 2. First Workflow, 3. API Key Connection]

PART 2: CREATING YOUR N8N ACCOUNT
------------------------

Go to n8n.io and click "Get started free." You can use the cloud version, which is the easiest option. Sign up with your email. The free tier gives you enough executions for all the labs in this course.

Once you are in, you will see the n8n dashboard. This is where all your workflows live. Right now it is empty. That is about to change.

If you prefer to self-host, you can run n8n locally with Docker. The command is: docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n. But for this course, the cloud version is perfectly fine.

[ANIMATION: Screen recording -- navigating to n8n.io, signing up, landing on the empty dashboard]

PART 3: BUILDING YOUR FIRST WORKFLOW
------------------------

Click "Add workflow" in the top right. You will see an empty canvas with a trigger node.

Every workflow starts with a trigger. This is what kicks off the workflow. It could be a schedule, a webhook, a new email, or a manual trigger. For now, click the trigger node and select "Manual Trigger." This lets you run the workflow by clicking a button.

Now add your first action node. Click the plus icon. Search for "HTTP Request." This node lets you call any API. Configure it with a simple GET request to a public API -- try httpbin.org/get. Click "Test step." You should see a JSON response.

That is it. You just built a workflow. A trigger that starts it. A node that does something. Everything else in n8n is just more nodes and more connections.

[ANIMATION: Screen recording -- creating workflow, adding manual trigger, adding HTTP Request node, testing it]

PART 4: CONNECTING YOUR OPENAI API KEY
------------------------

For the lab, you will need to connect n8n to OpenAI. Click on a new node, search for "OpenAI," and select it. The first time you use it, n8n will ask for your credentials.

Click "Create new credential." Paste your OpenAI API key. Give it a name like "DADS5250 OpenAI." Click save.

Now any node in any workflow can use this credential. You only set it up once.

Important: n8n stores credentials encrypted. But just like with Colab Secrets, never share your workflow exports publicly if they contain credential references.

[ANIMATION: Screen recording -- adding OpenAI node, creating credential, saving, showing the credential selector]

PART 5: COMMON ISSUES
------------------------

A few things that come up.

First: "Workflow execution failed -- timeout." This usually means your API call took too long. Check your prompt length and model selection. Use gpt-4.1-mini for faster responses.

Second: "Invalid API key." Double-check your credential. Go to the credentials page and verify the key is correct.

Third: nodes not connecting. Make sure you drag from the output dot of one node to the input dot of the next. The connection line should snap into place.

If you run into anything else, post in the discussion board with a screenshot of your workflow and the error message.

Good luck with the lab.

======================================================
DIGITAL MEDIA NOTES:
- Full screen recording for Parts 2-4 with cursor highlights and zoom-ins
- Show the credential encryption note as an overlay banner: "Credentials are stored encrypted -- never share workflow exports publicly"
- Common Issues: three-panel error/solution graphic for quick reference
- Consider adding chapter markers at each Part for easy navigation
======================================================
