import { format, parseISO, isValid } from 'date-fns';
import { vi, enUS } from 'date-fns/locale';

export const formatDate = (date: string | Date, formatStr = 'dd/MM/yyyy', locale = 'vi'): string => {
  try {
    const dateObj = typeof date === 'string' ? parseISO(date) : date;
    if (!isValid(dateObj)) return '';
    
    const localeObj = locale === 'vi' ? vi : enUS;
    return format(dateObj, formatStr, { locale: localeObj });
  } catch {
    return '';
  }
};

export const formatDateTime = (date: string | Date, locale = 'vi'): string => {
  return formatDate(date, 'dd/MM/yyyy HH:mm', locale);
};

export const formatTime = (date: string | Date, locale = 'vi'): string => {
  return formatDate(date, 'HH:mm', locale);
};

export const formatDateForInput = (date: string | Date): string => {
  try {
    const dateObj = typeof date === 'string' ? parseISO(date) : date;
    if (!isValid(dateObj)) return '';
    return format(dateObj, 'yyyy-MM-dd');
  } catch {
    return '';
  }
};

export const formatDateTimeForInput = (date: string | Date): string => {
  try {
    const dateObj = typeof date === 'string' ? parseISO(date) : date;
    if (!isValid(dateObj)) return '';
    return format(dateObj, "yyyy-MM-dd'T'HH:mm");
  } catch {
    return '';
  }
};

export const isDateInRange = (date: string | Date, startDate: string | Date, endDate: string | Date): boolean => {
  try {
    const dateObj = typeof date === 'string' ? parseISO(date) : date;
    const startObj = typeof startDate === 'string' ? parseISO(startDate) : startDate;
    const endObj = typeof endDate === 'string' ? parseISO(endDate) : endDate;
    
    return dateObj >= startObj && dateObj <= endObj;
  } catch {
    return false;
  }
};

export const getDaysBetween = (startDate: string | Date, endDate: string | Date): number => {
  try {
    const startObj = typeof startDate === 'string' ? parseISO(startDate) : startDate;
    const endObj = typeof endDate === 'string' ? parseISO(endDate) : endDate;
    
    const diffTime = Math.abs(endObj.getTime() - startObj.getTime());
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  } catch {
    return 0;
  }
};

export const getRelativeDate = (date: string | Date, locale = 'vi'): string => {
  try {
    const dateObj = typeof date === 'string' ? parseISO(date) : date;
    const now = new Date();
    const diffDays = Math.floor((dateObj.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
    
    if (locale === 'vi') {
      if (diffDays === 0) return 'Hôm nay';
      if (diffDays === 1) return 'Ngày mai';
      if (diffDays === -1) return 'Hôm qua';
      if (diffDays > 1) return `Sau ${diffDays} ngày`;
      if (diffDays < -1) return `${Math.abs(diffDays)} ngày trước`;
    } else {
      if (diffDays === 0) return 'Today';
      if (diffDays === 1) return 'Tomorrow';
      if (diffDays === -1) return 'Yesterday';
      if (diffDays > 1) return `In ${diffDays} days`;
      if (diffDays < -1) return `${Math.abs(diffDays)} days ago`;
    }
    
    return formatDate(dateObj, 'dd/MM/yyyy', locale);
  } catch {
    return '';
  }
};
