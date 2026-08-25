#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "tokens" / "icon-identity.json"
DOC = ROOT / "ICON_IDENTITY.md"


def fail(message: str) -> None:
    raise SystemExit(f"icon identity validation failed: {message}")


def main() -> None:
    if not TOKENS.is_file() or not DOC.is_file():
        fail("identity contract source files are missing")

    data = json.loads(TOKENS.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    if meta.get("status") != "candidate" or meta.get("stableBaseline") != "1.4.0":
        fail("identity system must remain a 1.5 Candidate over Stable 1.4.0")
    if data.get("principle") != "shared DNA without shared identity":
        fail("canonical identity principle changed unexpectedly")
    if data.get("hierarchy") != ["ecosystem", "family", "product", "state"]:
        fail("identity hierarchy must remain Ecosystem, Family, Product, State")

    ecosystem = data.get("ecosystem", {})
    if ecosystem.get("corporateMarkRequiredInProductIcons") is not False:
        fail("product icons must not require the corporate mark")

    dna = data.get("identityDNA", {})
    if dna.get("requiredForMajorFirstPartyProducts") is not True or dna.get("complementsIdentityLock") is not True:
        fail("major first-party products require Identity DNA that complements Identity Lock")

    required_families = {
        "communication", "productivity", "media", "cloud-and-data", "network", "security",
        "system-utility", "ai-and-intelligence", "browser-and-discovery", "persistence-and-resilience"
    }
    if set(data.get("families", {})) != required_families:
        fail("first-party family registry is incomplete")

    rules = data.get("familyRules", {})
    if rules.get("sameSymbolDifferentColorOnly") is not False:
        fail("families may not differentiate products only by color")
    if rules.get("primarySilhouetteMustRemainDistinct") is not True:
        fail("product silhouettes must remain distinct")

    colors = data.get("colorOwnership", {})
    for key in ["identityColorFamilyPerMajorProduct", "colorSecondaryToShape", "monochromeDifferentiationRequired", "protectedSemanticColorsOutsideProductOwnership"]:
        if colors.get(key) is not True:
            fail(f"color ownership invariant {key} must remain true")

    service = data.get("serviceDerivation", {})
    if service.get("copyApplicationIconDirectly") is not False:
        fail("service identities must not copy application icons directly")
    for key in ["mustUseServiceConstruction", "temporaryStateSeparateFromIdentity", "backgroundServicesPrioritizeCapabilityRecognition", "lowLevelInfrastructureUsesReducedSymbolicRepresentation"]:
        if service.get(key) is not True:
            fail(f"service derivation invariant {key} must remain true")

    third_party = data.get("thirdParty", {})
    if third_party.get("preserveIdentity") is not True or third_party.get("forceGoreeCloudFamilyMotifs") is not False or third_party.get("falseRebranding") is not False:
        fail("third-party identity protection changed unexpectedly")

    review = data.get("review", {})
    required_dimensions = {"recognition", "distinctiveness", "family-relationship", "glaze-coherence", "scalability", "accessibility", "longevity"}
    if set(review.get("dimensions", [])) != required_dimensions:
        fail("identity review dimensions are incomplete")
    if review.get("singleAutomatedScoreAuthoritative") is not False:
        fail("automated identity scoring must not override human judgment")

    collision = data.get("collisionDetection", {})
    if collision.get("status") != "planned" or collision.get("humanReviewFinalAuthority") is not True:
        fail("collision detection must remain Planned with human final authority")
    if data.get("ecosystemWall", {}).get("status") != "planned":
        fail("Ecosystem Wall must remain Planned until implemented")

    new_product = data.get("newProduct", {})
    for key in ["meaningBeforeAesthetics", "defineFamilyBeforeRendering", "defineDifferentiationBeforeRendering", "proposeIdentityLockBeforeRendering"]:
        if new_product.get(key) is not True:
            fail(f"new-product identity invariant {key} must remain true")

    redesign = data.get("redesign", {})
    if redesign.get("trendChangeAloneInsufficient") is not True or redesign.get("preferPresentationEvolutionBeforeIdentityReplacement") is not True:
        fail("redesign threshold must preserve identity continuity")

    relationship = data.get("applicationServiceRelationship", {})
    for key in ["applicationCommunicatesDestination", "serviceCommunicatesCapability", "sharedDNACommunicatesOwnership", "differentConstructionCommunicatesRole"]:
        if relationship.get(key) is not True:
            fail(f"application/service relationship invariant {key} must remain true")

    doc = DOC.read_text(encoding="utf-8")
    for phrase in [
        "shared DNA without shared identity",
        "Ecosystem → Family → Product → State",
        "Identity DNA",
        "Product color ownership",
        "Service derivation",
        "Collision detection",
        "Ecosystem Wall",
        "does not require or plan a dedicated Icon Studio application",
        "Candidate promotion boundary",
    ]:
        if phrase not in doc:
            fail(f"documentation invariant missing: {phrase}")

    print("Glaze UI icon identity Candidate validation passed")


if __name__ == "__main__":
    main()
