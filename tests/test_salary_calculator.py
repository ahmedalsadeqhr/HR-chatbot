import pytest

from salary_calculator import (
    _ANNUAL_EXEMPT,
    _SI_CAP,
    _SI_FLOOR,
    _SI_RATE,
    calculate_net_salary,
    extract_salary_amount,
    is_no_commission,
    is_salary_calc_request,
    salary_calc_context,
)


# ── calculate_net_salary ──────────────────────────────────────────────────────

class TestCalculateNetSalary:
    def test_gross_5000(self):
        r = calculate_net_salary(5_000)
        assert r["net"] == pytest.approx(4_447.50, abs=1)

    def test_gross_10000(self):
        r = calculate_net_salary(10_000)
        assert r["net"] == pytest.approx(8_302.50, abs=1)

    def test_gross_15000(self):
        r = calculate_net_salary(15_000)
        assert r["net"] == pytest.approx(11_860, abs=1)

    def test_gross_20000(self):
        r = calculate_net_salary(20_000)
        assert r["net"] == pytest.approx(15_708, abs=1)

    def test_gross_30000(self):
        r = calculate_net_salary(30_000)
        assert r["net"] == pytest.approx(23_457, abs=1)

    def test_gross_50000(self):
        r = calculate_net_salary(50_000)
        assert r["net"] == pytest.approx(38_618, abs=1)

    def test_si_cap_applied_above_16700(self):
        r = calculate_net_salary(20_000)
        assert r["insurable_wage"] == _SI_CAP
        assert r["monthly_si"] == pytest.approx(_SI_CAP * _SI_RATE, abs=0.01)

    def test_si_floor_applied_below_2700(self):
        r = calculate_net_salary(1_000)
        assert r["insurable_wage"] == _SI_FLOOR

    def test_si_within_range(self):
        r = calculate_net_salary(10_000)
        assert r["insurable_wage"] == 10_000

    def test_personal_exemption_is_20000(self):
        r = calculate_net_salary(5_000)
        assert r["personal_exemption"] == _ANNUAL_EXEMPT

    def test_zero_tax_below_threshold(self):
        # Annual gross 5000*12=60000, SI=6600, before_exempt=53400, taxable=33400 < 40000 → 0 tax
        r = calculate_net_salary(5_000)
        assert r["annual_tax"] == 0.0
        assert r["monthly_tax"] == 0.0

    def test_martyrs_fund_calculated(self):
        r = calculate_net_salary(10_000)
        assert r["monthly_martyrs"] == pytest.approx(5.0, abs=0.01)

    def test_net_formula(self):
        r = calculate_net_salary(10_000)
        expected = 10_000 - r["monthly_si"] - r["monthly_tax"] - r["monthly_martyrs"]
        assert r["net"] == pytest.approx(expected, abs=0.01)

    def test_effective_rate_positive_for_high_salary(self):
        r = calculate_net_salary(50_000)
        assert r["effective_rate"] > 0

    def test_effective_rate_zero_for_low_salary(self):
        r = calculate_net_salary(5_000)
        assert r["effective_rate"] == 0.0

    def test_breakdown_has_entries_when_taxable(self):
        r = calculate_net_salary(20_000)
        assert len(r["breakdown"]) > 0

    def test_no_tax_when_below_threshold(self):
        # Taxable income 33,400 < 40,000 — falls entirely in the 0% bracket
        r = calculate_net_salary(5_000)
        assert r["annual_tax"] == 0.0
        assert all(b["ضريبة"] == "0.00" for b in r["breakdown"])

    def test_invalid_salary_too_low(self):
        with pytest.raises(ValueError):
            calculate_net_salary(100)

    def test_invalid_salary_too_high(self):
        with pytest.raises(ValueError):
            calculate_net_salary(10_000_000)

    def test_invalid_salary_zero(self):
        with pytest.raises(ValueError):
            calculate_net_salary(0)

    def test_invalid_salary_negative(self):
        with pytest.raises(ValueError):
            calculate_net_salary(-5_000)

    def test_at_si_cap_boundary(self):
        r = calculate_net_salary(_SI_CAP)
        assert r["insurable_wage"] == _SI_CAP

    def test_annual_gross_equals_monthly_times_12(self):
        r = calculate_net_salary(8_000)
        assert r["annual_gross"] == 8_000 * 12

    def test_returns_dict_with_required_keys(self):
        r = calculate_net_salary(10_000)
        required = {
            "gross", "insurable_wage", "monthly_si", "monthly_martyrs",
            "annual_gross", "annual_si", "annual_taxable", "annual_tax",
            "monthly_tax", "net", "effective_rate", "breakdown",
        }
        assert required.issubset(r.keys())


# ── salary_calc_context ───────────────────────────────────────────────────────

class TestSalaryCalcContext:
    def test_returns_string(self):
        assert isinstance(salary_calc_context(10_000), str)

    def test_contains_net_salary(self):
        r = calculate_net_salary(10_000)
        ctx = salary_calc_context(10_000)
        assert f"{r['net']:,.2f}" in ctx

    def test_contains_gross(self):
        ctx = salary_calc_context(15_000)
        assert "15,000.00" in ctx


# ── extract_salary_amount ─────────────────────────────────────────────────────

class TestExtractSalaryAmount:
    def test_arabic_currency_suffix(self):
        assert extract_salary_amount("راتب 15000 جنيه") == 15_000.0

    def test_egp_suffix(self):
        assert extract_salary_amount("salary 12000 EGP") == 12_000.0

    def test_bare_number(self):
        assert extract_salary_amount("احسب صافي 20000") == 20_000.0

    def test_number_with_commas(self):
        assert extract_salary_amount("20,000 EGP") == 20_000.0

    def test_number_with_arabic_comma(self):
        assert extract_salary_amount("20،000 جنيه") == 20_000.0

    def test_decimal_salary(self):
        assert extract_salary_amount("salary 9500.50 EGP") == 9_500.50

    def test_below_minimum_returns_none(self):
        assert extract_salary_amount("100 EGP") is None

    def test_above_maximum_returns_none(self):
        assert extract_salary_amount("9999999 EGP") is None

    def test_no_number_returns_none(self):
        assert extract_salary_amount("كم يوم إجازة لديّ؟") is None

    def test_empty_string_returns_none(self):
        assert extract_salary_amount("") is None


# ── is_salary_calc_request ────────────────────────────────────────────────────

class TestIsSalaryCalcRequest:
    def test_arabic_trigger_with_number(self):
        assert is_salary_calc_request("احسب صافي راتب 15000") is True

    def test_english_trigger_with_number(self):
        assert is_salary_calc_request("calculate net salary 10000") is True

    def test_trigger_without_number(self):
        assert is_salary_calc_request("احسب الراتب") is False

    def test_number_without_trigger(self):
        assert is_salary_calc_request("لدي 15000 جنيه") is False

    def test_unrelated_question(self):
        assert is_salary_calc_request("كم يوم إجازة سنوية؟") is False

    def test_empty_string(self):
        assert is_salary_calc_request("") is False

    def test_whitespace_only(self):
        assert is_salary_calc_request("   ") is False


# ── is_no_commission ──────────────────────────────────────────────────────────

class TestIsNoCommission:
    def test_arabic_no(self):
        assert is_no_commission("لا") is True

    def test_english_no(self):
        assert is_no_commission("no") is True

    def test_zero_string(self):
        assert is_no_commission("0") is True

    def test_none_string(self):
        assert is_no_commission("none") is True

    def test_mafesh(self):
        assert is_no_commission("مفيش") is True

    def test_with_trailing_space_phrase(self):
        assert is_no_commission("no commission this month") is True

    def test_positive_number_is_not_no(self):
        assert is_no_commission("5000") is False

    def test_yes_is_not_no(self):
        assert is_no_commission("نعم") is False
