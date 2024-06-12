import type { Ruleset } from "@/def/typedef";
import osu_ruleset_osu from '@/assets/images/osu/rulesets/osu.svg';
import osu_ruleset_mania from '@/assets/images/osu/rulesets/mania.svg';
import osu_ruleset_taiko from '@/assets/images/osu/rulesets/taiko.svg';
import osu_ruleset_fruits from '@/assets/images/osu/rulesets/fruits.svg';

const rulesetIcons = {
    0: osu_ruleset_osu,
    1: osu_ruleset_taiko,
    2: osu_ruleset_fruits,
    3: osu_ruleset_mania,
}

export function asVanilla(ruleset: Ruleset | number) {
    if (ruleset == 8) return 0;
    if (ruleset >= 4) return ruleset - 4;
    return ruleset;
}

export function asIcon(ruleset: Ruleset | number) {
    ruleset = asVanilla(ruleset);
    return rulesetIcons[Number(ruleset) as keyof typeof rulesetIcons];
}