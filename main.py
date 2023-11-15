import argparse

def main():
    parser = argparse.ArgumentParser("alessandro")
    parser.add_argument("--mode", type=str, help="Alessandro mode (console|GUI)).")
    args = parser.parse_args()
    
    if args.mode == 'console':
        from alessandro import AlessandroBot
        ale_bot = AlessandroBot()
        ale_bot.ask(True)
    elif args.mode == 'GUI':
        from alessandro_avatar import AlessandroAvatarApp
        app = AlessandroAvatarApp()
        app.run()

if __name__ == '__main__':
    main()
