import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--chara", dest="chara", nargs="+", help="1 or 2 characters (png card of json file)")
    parser.add_argument("-d", "--dialog",dest="dialog", action='store_true', help="Automatic dialogue beetween 2 characters")
    parser.add_argument("-i", "--interactive", dest="interactive", action='store_true', help="Chat interactively with one character")
    parser.add_argument("-o", "--output", dest="output", help="Save the output to a file")
    args = parser.parse_args()

    if args.chara is None:
        print("Please specify at least one character!\n")
        parser.print_help()
        exit()

    if len(args.chara) > 2:
        print("Too much characters!\n")
        parser.print_help()
        exit()

    if args.dialog is True and args.interactive is True:
        print("Please specify a dialog or an interactive chat, not both!\n")
        parser.print_help()
        exit()

    if args.dialog is True and len(args.chara) != 2:
        print("Please specify 2 characters for a dialog!\n")
        parser.print_help()
        exit()

    if args.interactive is True and len(args.chara) != 1:
        print("Please specify 1 character for an interactive chat!\n")
        parser.print_help()
        exit()

    if args.interactive is True:
        if args.output is None:
            print("Please specify an output file!\n")
            parser.print_help()
            exit()
        return {
            "mode": "interactive",
            "chara1": args.chara[0],
            "output": args.output
        }

    if args.dialog is True:
        if args.output is None:
            print("Please specify an output file!\n")
            parser.print_help()
            exit()
        return {
            "mode": "dialog",
            "chara1": args.chara[0],
            "chara2": args.chara[1],
            "output": args.output
        }
    
    if len(args.chara) != 1:
        print("Please specify 1 character card for decode it!\n")
        parser.print_help()
        exit()

    if args.output is not None:
        print("Please do not specify an output file for character decoding!\n")
        parser.print_help()
        exit()

    return {
        "mode": "decode",
        "chara1": args.chara[0],
        "output": args.output
    }
    
