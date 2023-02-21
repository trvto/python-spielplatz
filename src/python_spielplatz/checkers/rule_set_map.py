from .checkerserror import CheckersError
from .rule_set_interface import RuleSet
from .standard_rule_set import StandardRuleSet

rule_set_dict = {
    "StandardRuleSet": StandardRuleSet(),
}


def get_rule_set(rule_set_str: str) -> RuleSet | CheckersError:
    """Get rule set object from a string."""
    rule_set = rule_set_dict.get(rule_set_str)
    if rule_set is None:
        return CheckersError(f"Requested rule set '{rule_set_str}' is not available")
    return rule_set
