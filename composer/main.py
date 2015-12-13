__author__ = 'juho'

import composer as c
import sys


def main(args):
    feedback_types = c.get_feedback_types()

    def collect_feedback():
        cmd = None
        feedback = {}
        while cmd != "q":
            for index, type in enumerate(feedback_types):
                print("{}: {}".format(index, type))
            cmd = input("Feedback? (q: quit, n: new)")
            if cmd == "n":
                category = input("Category name?")
                feedback[category] = input("Rating?")
            if cmd.isdigit():
                numeric_cmd = int(cmd)
                if 0 <= numeric_cmd <= len(feedback_types):
                    feedback[feedback_types[numeric_cmd]] = input("Rating?")
        return feedback

    if len(args) == 2:
        cmd = args[1]
        if cmd == "motiftrain":
            m = [c.random_motif(*c.bach_mcs())]
            notes = c.extract_notes(m)
            c.save_to_midi(notes)
            c.play_midi()
            c.save_rating(m, collect_feedback())
        elif cmd == "melodytrain":
            m = c.compose_music(40, feedback_types)
            notes = c.extract_notes(m)
            c.save_to_midi(notes)
            c.play_midi()
            c.save_rating(m, collect_feedback())
        elif cmd == "classic":
            m = c.get_classic()
            notes = c.extract_notes(m)
            c.save_to_midi(notes)
            c.play_midi()
            c.save_rating(m, collect_feedback())

    else:
        print("Needs one argument")
        print("motiftrain Train short melody")
        print("melodytrain Train longer melody")
        print("classic Play something with good rating")

if __name__ == "__main__": main(sys.argv)
