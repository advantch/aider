# aider is AI pair programming in your terminal

Aider is a command line tool that lets you pair program with GPT-3.5/GPT-4,
to edit code stored in your local git repository.
You can start a new project or work with an existing repo.
Aider makes sure edits from GPT are
[committed to git](https://aider.chat/docs/faq.html#how-does-aider-use-git)
with sensible commit messages.
Aider is unique in that it lets you ask for changes to [pre-existing, larger codebases](https://aider.chat/docs/repomap.html).

<p align="center">
  <img src="assets/screencast.svg" alt="aider screencast">
</p>

<p align="center">
  <a href="https://discord.gg/Tv2uQnR88V">
    <img src="https://img.shields.io/badge/Join-Discord-blue.svg"/>
  </a>
</p>

- [Getting started](#getting-started)
- [Example chat transcripts](#example-chat-transcripts)
- [Features](#features)
- [Usage](#usage)
- [In-chat commands](#in-chat-commands)
- [Tips](#tips)
- [GPT-4 vs GPT-3.5](https://aider.chat/docs/faq.html#gpt-4-vs-gpt-35)
- [Claude models](#claude-models)
- [Installation](https://aider.chat/docs/install.html)
- [Voice-to-code](https://aider.chat/docs/voice.html)
- [FAQ](https://aider.chat/docs/faq.html)
- [Discord](https://discord.gg/Tv2uQnR88V)

## New GPT-4 Turbo with 128k context window

Aider supports OpenAI's new GPT-4 model that has the massive 128k context window.
Early benchmark results
indicate that it is
[very fast](https://aider.chat/docs/benchmarks-speed-1106.html)
and a bit
[better at coding](https://aider.chat/docs/benchmarks-1106.html)
than previous GPT-4 models.

To use it, run aider like this:

```
aider --model gpt-4-1106-preview
```

## Claude models

Aider now supports Anthropic's Claude models, which offer large context windows and strong coding capabilities.

To use Claude models, you'll need an Anthropic API key. You can set it using the `--anthropic-api-key` parameter or by setting the `ANTHROPIC_API_KEY` environment variable.

Available Claude models:
- Claude 3 Opus: `claude-3-opus-20240229` (200k tokens)
- Claude 3 Sonnet: `claude-3-sonnet-20240229` (180k tokens)
- Claude 3 Haiku: `claude-3-haiku-20240307` (150k tokens)
- Claude 2.1: `claude-2.1` (100k tokens)
- Claude 2.0: `claude-2.0` (100k tokens)
- Claude Instant 1.2: `claude-instant-1.2` (100k tokens)

To use Claude 3 Sonnet, run:

```
aider --anthropic-api-key your_api_key --model claude-3-sonnet-20240229
```

Or use the shorthand flags:

```
aider --anthropic-api-key your_api_key --claude-sonnet
```

## Getting started
