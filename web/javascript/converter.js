converter = {
    // Note is of form ["c", "16], where the first cell is the key and second the duration
    convert: function (note) {
        return new Vex.Flow.StaveNote({
                keys: [convertKeyToVexflow(note[0])],
                duration: convertDurationToVexflow(note[1])
            });
    },

    // Key is in Lilypond form, e.g. c, c'' or c,,
    convertKey: function convertKeyToVexflow(key) {
        // For rests we define here only the visual position of the note
        if (key === "r") {
            return "b/4";
        }
        // Lilypond uses ' and , to notate different height of the same note
        var ups = key.split("'").length - 1;
        var downs = key.split(",").length - 1;
        // c/4 matches Lilypond c
        var height = 4 + ups - downs;
        return key.charAt(0) + "/" + height;
    },

    // Duration is in Lilypond form, e.g. 16, 8 or 2. We need here the key as well, since rests are marked in duration in vexflow
    convertDuration: function (key, duration) {
        var suffix = key === "r" ? "r" : "";
        return duration + suffix;
    }
};


