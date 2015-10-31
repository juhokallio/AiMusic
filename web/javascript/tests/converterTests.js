/**
 * Unit tests for Lilypond -> vexflow converter
 */

QUnit.test("Note conversion test", function(assert) {
  assert.equal(converter.convertKey("c"), "c/4", "Basic c note");
  assert.equal(converter.convertKey("d'"), "d/5", "d note up one octave");
  assert.equal(converter.convertKey("e,,"), "e/2", "e note down two octaves");
  assert.equal(converter.convertKey("r"), "b/4", "Rest conversion (only for visual position)");
});

QUnit.test("Duration conversion test", function(assert) {
  assert.equal(converter.convertDuration("c", "16"), "16", "16 duration");
  assert.equal(converter.convertDuration("r", "16"), "16r", "16 rest duration");
});
