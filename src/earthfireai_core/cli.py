import argparse

from .client import OllamaClient, OllamaError


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="earthfire-local-ai")
    commands = result.add_subparsers(dest="command", required=True)
    commands.add_parser("status", help="检查 Ollama 状态")
    commands.add_parser("models", help="列出本地模型")
    chat = commands.add_parser("chat", help="发送一次非流式对话")
    chat.add_argument("prompt")
    chat.add_argument("--system")
    chat.add_argument("--model")
    return result


def main(argv=None) -> int:
    args = parser().parse_args(argv)
    client = OllamaClient()
    try:
        if args.command == "status":
            print(f"Ollama 已连接，版本 {client.version()}")
        elif args.command == "models":
            print("
".join(client.models()) or "没有发现本地模型")
        else:
            print(client.chat(args.prompt, system=args.system, model=args.model))
        return 0
    except (OllamaError, ValueError) as exc:
        print(f"错误：{exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
