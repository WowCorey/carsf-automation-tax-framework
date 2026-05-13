# Formula Reference

All formulas are concept-level and use placeholder schedule parameters until calibrated with real data.

## Qualified Labour Contribution

```text
FTE_worker = annual_hours / full_time_hours

QLC_worker = min(
    FTE_worker * (1 + alpha*WQ + beta*JS + gamma*SD + delta*AN),
    FTE_worker * QLCMaxMultiplier
)

QLC_firm = sum(QLC_worker)
```

## Output-per-FTE Benchmark

```text
OPFTE_LIBC = CanonicalOutput_LIBC / QLC_LIBC
```

## Human Labour Equivalent

```text
HLE = Output_firm / OPFTE_LIBC
```

## Automation Intensity Index

```text
AII = w1*ComputeRatio
    + w2*AutoDecisionRatio
    + w3*RoboticsCapitalRatio
    + w4*AutoProcessShare
```

Components are bounded in `[0, 1]`, weights sum to 1, and AII is bounded in `[0, 1]`.

## Net Labour Tax Gap

```text
NLTG = max(0, (HLE * AII) - QLC)
```

## Australian Automated Value Added

```text
AAVA = AustralianAttributableRevenue
     - VerifiedNonAutomationInputCosts
     - VerifiedQLC_WageCost
```

The AAVA deductibility schedule is not final.

See `paper/aava_deductibility_appendix.md` for the V1.5 prototype taxonomy.

## Automation Equilibrium Levy

```text
AEL_raw = NLTG * FRV_standard
AEL_payable = min(AEL_raw, lambda_sector * AAVA)
Shortfall = AEL_raw - AEL_payable
```

## Automation Rent Levy

```text
ARL = max(0, AAVA - (UpliftRate * CapitalBase)) * RentTaxRate
```

This is PRRT-inspired uplift logic, not a full PRRT model.

## Credits and Caps

```text
Credits = min(VerifiedCredits, theta * (AEL_payable + ARL))
CombinedLiability = AEL_payable + ARL - Credits
Liability = min(CombinedLiability, LAMBDA_sector * AAVA)
```

## Coverage Measures

```text
CARS_I = NationalAutomationFiscalDamage / (AutomationRevenueCaptured + epsilon)
CoverageRatio = AutomationRevenueCaptured / NationalAutomationFiscalDamage
```

Zero-damage and zero-revenue periods require explicit safe handling.

For policy-facing reporting, CoverageRatio is `N/A - no measured damage` when NationalAutomationFiscalDamage is zero. It must not be displayed as 100% coverage.
