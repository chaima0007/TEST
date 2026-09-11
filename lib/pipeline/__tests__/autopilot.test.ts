import { describe, it, expect } from "vitest";
import { meetsLevel } from "../autopilot";

describe("meetsLevel", () => {
  it("au niveau 'strong', seules les recos 'strong' qualifient", () => {
    expect(meetsLevel("strong", "strong")).toBe(true);
    expect(meetsLevel("consider", "strong")).toBe(false);
    expect(meetsLevel("skip", "strong")).toBe(false);
  });

  it("au niveau 'consider', 'strong' et 'consider' qualifient", () => {
    expect(meetsLevel("strong", "consider")).toBe(true);
    expect(meetsLevel("consider", "consider")).toBe(true);
    expect(meetsLevel("skip", "consider")).toBe(false);
  });
});
