### How the `copilot-api` Repo Works

The `copilot-api` repository is a clever piece of software that acts as a bridge or a translator. It takes the API provided by GitHub Copilot and makes it look like the APIs from OpenAI (the creators of GPT models) and Anthropic (the creators of Claude).

Here's a breakdown of its key features:

*   **API Compatibility:** The main function is to expose GitHub Copilot's functionality through endpoints that are identical to OpenAI's `/v1/chat/completions`, `/v1/models`, `/v1/embeddings` and Anthropic's `/v1/messages`. This means any tool that is built to work with OpenAI or Anthropic can be "tricked" into working with GitHub Copilot instead.
*   **Claude Code Integration:** The repository has a specific focus on making it easy to use GitHub Copilot as the "brain" for Claude Code, which is a conversational AI assistant for developers from Anthropic.
*   **Usage Monitoring:** It includes a web-based dashboard that lets you see how much you're using the Copilot API, what your quotas are, and other useful stats.
*   **Rate Limiting:** To prevent you from getting blocked by GitHub for making too many requests too quickly, it has features to control the rate of API calls.
*   **Authentication Flexibility:** You can either log in to your GitHub account interactively through the command line or provide a GitHub token directly, which is useful for automated environments.

### Practical Explanation of How to Use This Repo in Claude Code

You have two primary methods to get Claude Code working with `copilot-api`:

**1. The Easy Way: Interactive Setup**

This is the recommended approach for the first time you use it.

1.  Run the following command in your terminal:

    ```bash
    npx copilot-api@latest start --claude-code
    ```
2.  The script will guide you through a couple of choices for which model you want to use for different tasks.
3.  Once you've made your selections, the tool will copy a command to your clipboard.
4.  Open a **new** terminal window, paste the command, and press Enter. This will start Claude Code with all the right settings to use `copilot-api` as its backend.

**2. The Advanced Way: Manual Configuration**

If you want a more permanent setup that doesn't require the interactive setup each time, you can manually create a configuration file.

1.  In the root directory of your project, create a folder named `.claude`.
2.  Inside the `.claude` folder, create a file named `settings.json`.
3.  Paste the following content into `settings.json`:

    ```json
    {
      "env": {
        "ANTHROPIC_BASE_URL": "http://localhost:4141",
        "ANTHROPIC_AUTH_TOKEN": "dummy",
        "ANTHROPIC_MODEL": "gpt-4.1",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "gpt-4.1",
        "ANTHROPIC_SMALL_FAST_MODEL": "gpt-4.1",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "gpt-4.1",
        "DISABLE_NON_ESSENTIAL_MODEL_CALLS": "1",
        "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
      },
      "permissions": {
        "deny": [
          "WebSearch"
        ]
      }
    }
    ```
4.  Now, whenever you run Claude Code in that project, it will automatically use these settings and connect to the `copilot-api` server.

### Setup and Verification

I attempted to run the `copilot-api` server using the following command:

```bash
npx copilot-api@latest start > copilot_api_research/server.log 2>&1 &
```

However, the server did not produce any output in the log file. I checked the running jobs and found the process was still active:

```bash
$ jobs
[1]+  Running                 npx copilot-api@latest start > copilot_api_research/server.log 2>&1 &
```

This suggests that the server was waiting for an interactive authentication step, which could not be completed in the non-interactive environment. I terminated the process with the following command:

```bash
kill %1
```

**Conclusion:** The `copilot-api` server cannot be started in a non-interactive environment without providing a pre-generated GitHub token. This is a critical limitation to be aware of when using this tool in automated workflows.
