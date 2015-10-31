var sampleMusic = [{"notes": [["r", "16"], ["c", "16"], ["a,", "8"], ["e", "8"]], "type": "motif"}];

$(document).ready(function() {
    var renderer = new Vex.Flow.Renderer("notation", Vex.Flow.Renderer.Backends.CANVAS);

    var ctx = renderer.getContext();
    var stave = new Vex.Flow.Stave(10, 0, 500);
    stave.addClef("treble").setContext(ctx).draw();
});
