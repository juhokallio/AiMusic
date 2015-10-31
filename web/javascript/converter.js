converter = {
    // Note is of form ["c", "16], where the first cell is the key and second the duration
    convertToVexflow: function (note) {
        return new Vex.Flow.StaveNote({
                keys: [convertKeyToVexflow(note[0])],
                duration: convertDurationToVexflow(note[1])
            });
    },

    // Key is in Lilypond form, e.g. c, c'' or c,,
    convertKeyToVexflow: function convertKeyToVexflow(key) {
        // Lilypond uses ' and , to notate different height of the same note
        var ups = key.split("'").length - 1;
        var downs = key.split(",").length - 1;
        // c/4 matches Lilypond c
        var height = 4 + ups - downs;
        return key.charAt(0) + "/" + height;
    },

    // Duration is in Lilypond form, e.g. 16, 8 or 2
    convertDurationToVexflow: function (duration) {
    }
};


