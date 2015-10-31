var sampleMusic = [{"notes": [["r", "16"], ["c", "16"], ["a,", "8"], ["e", "8"]], "type": "motif"}];

$(document).ready(function() {
    var renderer = new Vex.Flow.Renderer("notation", Vex.Flow.Renderer.Backends.CANVAS);

    var ctx = renderer.getContext();
    var stave = new Vex.Flow.Stave(10, 0, 500);
    stave.addClef("treble").setContext(ctx).draw();

    var notes = _.map(sampleMusic[0].notes, converter.convert);

    // Create a voice in 4/4
    var voice = new Vex.Flow.Voice({
        num_beats: 4,
        beat_value: 4,
        resolution: Vex.Flow.RESOLUTION
    });
    // The API is kind of meh here, this has to be specified separately outside the initialization.
    voice.setStrict(false);

    // Add notes to voice
    voice.addTickables(notes);

    // Format and justify the notes to 500 pixels
    var formatter = new Vex.Flow.Formatter().
    joinVoices([voice]).format([voice], 500);

    // Render voice
    voice.draw(ctx, stave);
});
