import { CurrencyEnum } from '../types';

export const formatCurrency = (
  amount: number,
  currency: CurrencyEnum = CurrencyEnum.VND,
  locale = 'vi-VN'
): string => {
  try {
    const formatter = new Intl.NumberFormat(locale, {
      style: 'currency',
      currency: currency,
      minimumFractionDigits: currency === CurrencyEnum.VND ? 0 : 2,
      maximumFractionDigits: currency === CurrencyEnum.VND ? 0 : 2,
    });
    
    return formatter.format(amount);
  } catch {
    // Fallback formatting
    const symbols: Record<CurrencyEnum, string> = {
      [CurrencyEnum.VND]: '₫',
      [CurrencyEnum.USD]: '$',
      [CurrencyEnum.EUR]: '€',
      [CurrencyEnum.JPY]: '¥',
      [CurrencyEnum.KRW]: '₩',
      [CurrencyEnum.THB]: '฿',
    };
    
    const formattedAmount = amount.toLocaleString(locale);
    return `${formattedAmount} ${symbols[currency]}`;
  }
};

export const parseCurrencyInput = (input: string): number => {
  // Remove all non-digit and non-decimal point characters
  const cleanInput = input.replace(/[^\d.,]/g, '');
  
  // Handle different decimal separators
  const normalizedInput = cleanInput.replace(',', '.');
  
  const parsed = parseFloat(normalizedInput);
  return isNaN(parsed) ? 0 : parsed;
};

export const roundAmount = (amount: number, roundingRule: number = 1000): number => {
  if (roundingRule <= 1) {
    return Math.round(amount * 100) / 100; // Round to 2 decimal places
  }
  
  return Math.round(amount / roundingRule) * roundingRule;
};

export const calculatePercentage = (part: number, total: number): number => {
  if (total === 0) return 0;
  return (part / total) * 100;
};

export const convertCurrency = (
  amount: number,
  fromCurrency: CurrencyEnum,
  toCurrency: CurrencyEnum,
  exchangeRate: number = 1
): number => {
  if (fromCurrency === toCurrency) return amount;
  return amount * exchangeRate;
};

export const getCurrencySymbol = (currency: CurrencyEnum): string => {
  const symbols: Record<CurrencyEnum, string> = {
    [CurrencyEnum.VND]: '₫',
    [CurrencyEnum.USD]: '$',
    [CurrencyEnum.EUR]: '€',
    [CurrencyEnum.JPY]: '¥',
    [CurrencyEnum.KRW]: '₩',
    [CurrencyEnum.THB]: '฿',
  };
  
  return symbols[currency] || currency;
};

export const getDefaultCurrencyForLocale = (locale: string): CurrencyEnum => {
  const currencyMap: Record<string, CurrencyEnum> = {
    'vi': CurrencyEnum.VND,
    'vi-VN': CurrencyEnum.VND,
    'en-US': CurrencyEnum.USD,
    'en': CurrencyEnum.USD,
    'ja': CurrencyEnum.JPY,
    'ko': CurrencyEnum.KRW,
    'th': CurrencyEnum.THB,
  };
  
  return currencyMap[locale] || CurrencyEnum.VND;
};

export const formatCompactCurrency = (
  amount: number,
  currency: CurrencyEnum = CurrencyEnum.VND,
  locale = 'vi-VN'
): string => {
  const symbol = getCurrencySymbol(currency);
  
  if (amount >= 1000000000) {
    return `${(amount / 1000000000).toFixed(1)}B ${symbol}`;
  } else if (amount >= 1000000) {
    return `${(amount / 1000000).toFixed(1)}M ${symbol}`;
  } else if (amount >= 1000) {
    return `${(amount / 1000).toFixed(1)}K ${symbol}`;
  }
  
  return formatCurrency(amount, currency, locale);
};
