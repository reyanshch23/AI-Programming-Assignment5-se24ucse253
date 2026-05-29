# bayesian_network.py

P_study = {True: 0.6, False: 0.4}
P_difficult = {True: 0.4, False: 0.6}

P_grade_good = {
    (True,  True):  0.5,
    (True,  False): 0.9,
    (False, True):  0.1,
    (False, False): 0.4,
}

P_pass_given_grade = {True: 0.9, False: 0.2}

def joint_prob(study, difficult, grade_good, passed):
    """Compute the joint probability of a full assignment."""
    p = 1.0
    p *= P_study[study]
    p *= P_difficult[difficult]

    p_grade = P_grade_good[(study, difficult)]
    if not grade_good:
        p_grade = 1 - p_grade
    p *= p_grade

    p_pass = P_pass_given_grade[grade_good]
    if not passed:
        p_pass = 1 - p_pass
    p *= p_pass

    return p

def marginal(query_var, evidence=None):
    """
    Compute P(query_var | evidence) by summing over all other variables.
    query_var: dict like {'passed': True}
    evidence: dict like {'study': True}
    """
    vars_list = ['study', 'difficult', 'grade_good', 'passed']
    all_combos = []

    for s in [True, False]:
        for d in [True, False]:
            for g in [True, False]:
                for p in [True, False]:
                    all_combos.append({'study': s, 'difficult': d,
                                       'grade_good': g, 'passed': p})

    def matches(combo, conditions):
        if conditions is None:
            return True
        return all(combo[k] == v for k, v in conditions.items())

    numerator = 0.0
    denominator = 0.0
    joint_evidence_and_query = {**(evidence or {}), **query_var}

    for combo in all_combos:
        jp = joint_prob(combo['study'], combo['difficult'],
                        combo['grade_good'], combo['passed'])
        if matches(combo, evidence):
            denominator += jp
        if matches(combo, joint_evidence_and_query):
            numerator += jp

    if denominator == 0:
        return 0.0
    return numerator / denominator

def run_tests():
    print("===== Bayesian Network: Student Exam Model =====")
    print()
    print("Network: Study -> Grade <- Difficult -> ... Grade -> Pass")
    print()

    # Test 1: P(Pass = True)
    p = marginal({'passed': True})
    print(f"P(Pass = True)                    = {p:.4f}")

    # Test 2: P(Pass = True | Study = True)
    p = marginal({'passed': True}, evidence={'study': True})
    print(f"P(Pass=True | Study=True)         = {p:.4f}")

    # Test 3: P(Pass = True | Study = False)
    p = marginal({'passed': True}, evidence={'study': False})
    print(f"P(Pass=True | Study=False)        = {p:.4f}")

    # Test 4: P(Pass = True | Study = True, Difficult = True)
    p = marginal({'passed': True}, evidence={'study': True, 'difficult': True})
    print(f"P(Pass=True | Study=T, Diff=T)    = {p:.4f}")

    # Test 5: P(Pass = True | Study = True, Difficult = False)
    p = marginal({'passed': True}, evidence={'study': True, 'difficult': False})
    print(f"P(Pass=True | Study=T, Diff=F)    = {p:.4f}")

    # Test 6: Verify probabilities sum to 1
    p_true = marginal({'passed': True})
    p_false = marginal({'passed': False})
    print(f"\nSanity check: P(Pass=T) + P(Pass=F) = {p_true + p_false:.4f}  (should be 1.0)")

    # Test 7: Grade distribution
    p_g = marginal({'grade_good': True})
    print(f"P(Grade = Good)                   = {p_g:.4f}")

    # Test 8: What is the probability studying is hard?
    p_diff = marginal({'difficult': True}, evidence={'grade_good': False})
    print(f"P(Difficult=T | Grade=Bad)        = {p_diff:.4f}")

    print()
    print("--- Interpretation ---")
    print("Studying increases pass probability as expected.")
    print("Hard exams reduce grade quality.")
    print("Knowing the grade gives info about difficulty (explaining away).")

def print_full_joint():
    print("\n===== Full Joint Distribution =====")
    print(f"{'Study':<7} {'Diff':<7} {'Grade':<7} {'Pass':<7} {'Prob':<10}")
    print("-" * 40)
    total = 0.0
    for s in [True, False]:
        for d in [True, False]:
            for g in [True, False]:
                for p in [True, False]:
                    jp = joint_prob(s, d, g, p)
                    total += jp
                    print(f"{str(s):<7} {str(d):<7} {str(g):<7} {str(p):<7} {jp:.6f}")
    print(f"{'Total':<30} {total:.6f}  (should be 1.0)")

if __name__ == '__main__':
    run_tests()
    print_full_joint()
