/**
 * Unit tests for Lilypond -> vexflow converter
 */

QUnit.test("Note conversion test", function(assert) {
  assert.equal(converter.convertKeyToVexflow("c"), "c/4", "Basic c note was converted correctly");
});
