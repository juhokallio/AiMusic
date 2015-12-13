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
var ctx, stave, notes, critic, voice;

function getNotes() {
    var music = JSON.parse($("#music").html().trim());
    return _(music)
        .pluck("notes")
        .flatten()
        .map(converter.convert)
        .value();
}

$(document).ready(function() {
    notes = getNotes();
    critic = JSON.parse($("#critic").html().trim()) || _.map(notes, function(n) {
        return -1;
    });

    var renderer = new Vex.Flow.Renderer("notation", Vex.Flow.Renderer.Backends.CANVAS);
    ctx = renderer.getContext();
    stave = new Vex.Flow.Stave(10, 0, 1000);

    stave.addClef("treble").setContext(ctx).draw();

    draw();
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
    }
    draw();
}

function draw() {
    for (var i = 0; i < notes.length; i++) {
        var color = critic[i] === -1 ? "black" : labelColors[critic[i]];

        notes[i].setStyle({
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
    joinVoices([voice]).format([voice], 1000);
    ctx.clearRect(0, 0, 1000, 1000);
    stave.draw();
    voice.draw(ctx, stave);
}

function saveCritic(musicIndex, csrf) {
    $.post("/training/" + musicIndex + "/save", {
        "critic": JSON.stringify(critic),
        "csrfmiddlewaretoken": csrf
    });
}
