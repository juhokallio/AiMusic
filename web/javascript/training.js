var sampleMusic = [{"notes": [["r", "16"], ["c", "16"], ["a,", "8"], ["e", "8"]], "type": "motif"}];
var sampleCriticSubjects = [
    "rythm",
    "harmony",
    "ending",
    "feeling"
];

var labelColors = [
    "#00FF7F",
    "#FF8C00",
    "#8968CD",
    "#F08080"
];
var notes = _.map(sampleMusic[0].notes, converter.convert);
var ctx, stave;

var voice = new Vex.Flow.Voice({
    num_beats: 4,
    beat_value: 4,
    resolution: Vex.Flow.RESOLUTION
});

// The API is kind of meh here, this has to be specified separately outside the initialization.
voice.setStrict(false);

$(document).ready(function() {
    var renderer = new Vex.Flow.Renderer("notation", Vex.Flow.Renderer.Backends.CANVAS);
    ctx = renderer.getContext();
    stave = new Vex.Flow.Stave(10, 0, 500);

    stave.addClef("treble").setContext(ctx).draw();


    // Add notes to voice
    voice.addTickables(notes);

    // Format and justify the notes to 500 pixels
    var formatter = new Vex.Flow.Formatter().
    joinVoices([voice]).format([voice], 500);

    // Render voice
    voice.draw(ctx, stave);

    $("canvas#notation").click(handleClick);
    for(var i = 0; i < sampleCriticSubjects.length; i++) {
        appendLabel(sampleCriticSubjects[i], labelColors[i]);
    }
});

function appendLabel(label, color) {
    $("#criticTags").append("<div style='background-color: " + color + ";'>" + label + "</div>");
}

function alterNote(index) {
    notes[index] = new Vex.Flow.StaveNote({
                    keys: ["c/4"],
                    duration: "8"
                });
    voice.draw(ctx, stave);
}
alterNote(0);
critic = _.map(notes, function(n) {
    return -1;
});
function handleClick(event) {
    var x = event.offsetX;
    var y = event.offsetY;

    var affected = _.findIndex(notes, function (n) {
        var area = n.getBoundingBox();
        return x >= area.x
            && x <= area.x + area.w
            && y >= area.y
            && y <= area.y + area.h;
    });

    if (affected !== -1) {
        critic[affected]++;
        if (critic[affected] === sampleCriticSubjects.length) {
            critic[affected] = -1;
        }
        var color = critic[affected] === -1 ? "black" : labelColors[critic[affected]];

        notes[affected].setStyle({
            fillStyle: color,
            strokeStyle: color
        });
    }
    voice = new Vex.Flow.Voice({
        num_beats: 4,
        beat_value: 4,
        resolution: Vex.Flow.RESOLUTION
    });
    voice.setStrict(false);
    voice.addTickables(notes);
    var formatter = new Vex.Flow.Formatter().
    joinVoices([voice]).format([voice], 500);
    ctx.clearRect(0, 0, 500, 500);
    //console.log("asd" + affected.getBoundingBox());
    stave.draw();
    voice.draw(ctx, stave);
}

function hitsNote(note, x, y) {

}
