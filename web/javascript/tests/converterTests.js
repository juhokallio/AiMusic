/**
 * Unit tests for Lilypond -> vexflow converter
 */

QUnit.test("Note conversion test", function(assert) {
  assert.equal(converter.convertKeyToVexflow("c"), "c/4", "Basic c note");
  assert.equal(converter.convertKeyToVexflow("d'"), "d/5", "d note up one octave");
  assert.equal(converter.convertKeyToVexflow("e,,"), "e/2", "e note down two octaves");
});
