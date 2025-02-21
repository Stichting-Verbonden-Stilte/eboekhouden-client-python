"""This module contains enums for e-Boekhouden."""

from enum import Enum


# eboekhouden


class DateFilterOperator(Enum):
    """
    Enum class representing different date filter operators.
    Attributes:
        EQ (str): Equal to operator.
        NOT_EQ (str): Not equal to operator.
        GT (str): Greater than operator.
        GTE (str): Greater than or equal to operator.
        LT (str): Less than operator.
        LTE (str): Less than or equal to operator.
        RANGE (str): Range operator Between two values / dates.
    """

    EQ = "eq"
    NOT_EQ = "not_eq"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    RANGE = "range"


class MutationType(Enum):
    """
    Enum representing different types of financial mutations.
    Attributes:
        UNK (str): Represents an unknown mutation type.
        _1 (str): Represents an invoice received.
        _2 (str): Represents an invoice sent.
        _3 (str): Represents an invoice payment received.
        _4 (str): Represents an invoice payment sent.
        _5 (str): Represents money received.
        _6 (str): Represents money sent.
        _7 (str): Represents a general journal entry.
    """

    UNK = "Unknown"
    _1 = "Invoice Received"
    _2 = "Invoice Sent"
    _3 = "Invoice Payment Received"
    _4 = "Invoice Payment Sent"
    _5 = "Money Received"
    _6 = "Money Sent"
    _7 = "General Journal Entry"


class LedgerCategory(Enum):
    """
    Enum class representing different ledger categories.
    Attributes:
        UNK (str): Unknown category.
        BAL (str): Balance category.
        VW (str): Profit and loss category.
        AF6 (str): Turnover tax low rate category.
        AF19 (str): Turnover tax high rate category.
        AFOVERIG (str): Turnover tax other category.
        VOOR (str): Input tax category.
        BTWRC (str): VAT current account category.
        FIN (str): Liquid Assets category.
        DEB (str): Debtors category.
        CRED (str): Creditors category.
        AF (str): Turnover tax category.
    """

    UNK = "Unknown"
    BAL = "Balance"
    VW = "Profit and loss"
    AF6 = "Turnover tax low rate"
    AF19 = "Turnover tax high rate"
    AFOVERIG = "Turnover tax other"
    VOOR = "Input tax"
    BTWRC = "VAT current account"
    FIN = "Liquid Assets"
    DEB = "Debtors"
    CRED = "Creditors"
    AF = "Turnover tax"


class VATCodes(Enum):
    """
    Enum class representing various VAT (Value Added Tax) codes and their descriptions.
    Note:
        This enum needs to be updated when new groupings are created in e-Boekhouden.

    Attributes:
        HOOG_VERK_21 (str): For selling with 21% VAT.
        LAAG_VERK_9 (str): For selling with 9% VAT.
        VERL_VERK (str): For selling with reverse-charging 21% VAT.
        VERL_VERK_L9 (str): For selling with reverse-charging 9% VAT.
        AFW (str): VAT percentage is unspecified. Price values will be used.
        BU_EU_VERK (str): Deliveries outside the EU, 0% VAT.
        BI_EU_VERK (str): Goods inside the EU, 0% VAT.
        BI_EU_VERK_D (str): Services inside the EU, 0% VAT.
        AFST_VERK (str): Distance sales inside the EU, 0% VAT.
        LAAG_INK_9 (str): For buying with 9% VAT.
        HOOG_INK_21 (str): For buying with 21% VAT.
        VERL_INK (str): For buying with reverse-charging VAT.
        AFW_VERK (str): For selling with unspecified VAT percentage. Price values will be used.
        BU_EU_INK (str): For buying goods/services from outside the EU, 0% VAT.
        BI_EU_INK (str): For buying goods/services from inside the EU, 0% VAT.
        GEEN (str): No VAT.
    """

    HOOG_VERK_21 = "For selling with 21% VAT."
    LAAG_VERK_9 = "For selling with 9% VAT."
    VERL_VERK = "For selling with reverse-charging 21% VAT."
    VERL_VERK_L9 = "For selling with reverse-charging 9% VAT."
    AFW = "VAT percentage is unspecified. Price values will be used"
    BU_EU_VERK = "Deliveries outside the EU, 0% VAT."
    BI_EU_VERK = "Goods inside the EU, 0% VAT."
    BI_EU_VERK_D = "Services inside the EU, 0% VAT."
    AFST_VERK = "Distance sales inside the EU, 0% VAT."
    LAAG_INK_9 = "For buying with 9% VAT."
    HOOG_INK_21 = "For buying with 21% VAT."
    VERL_INK = "For buying with reverse-charging VAT."
    AFW_VERK = "For selling with unspecified VAT percentage. Price values will be used."
    BU_EU_INK = "For buying goods/services from outside the EU, 0% VAT."
    BI_EU_INK = "For buying goods/services from inside the EU, 0% VAT."
    GEEN = "No VAT."
