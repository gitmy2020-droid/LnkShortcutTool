import sys
import argparse
from gui import LnkShortcutGUI

def main():
    parser = argparse.ArgumentParser(description="LNK Shortcut Creator - Security Tool")
    parser.add_argument("-path", help="Local path to save the shortcut")
    parser.add_argument("-ip", help="SMB server IP or domain")
    parser.add_argument("-share", help="Shared folder name")
    parser.add_argument("-file", help="Target file name on SMB server")
    parser.add_argument("-icon", help="Icon file path (optional)")
    parser.add_argument("-gui", action="store_true", help="Run GUI mode")

    args = parser.parse_args()

    if args.gui or len(sys.argv) == 1:
        app = LnkShortcutGUI()
        app.mainloop()
    else:
        from lnk_creator import LnkCreator
        if not all([args.path, args.ip, args.share, args.file]):
            parser.print_help()
            sys.exit(1)
        creator = LnkCreator()
        success, message = creator.create_shortcut(args.path, args.ip, args.share, args.file, args.icon)
        print(message)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
