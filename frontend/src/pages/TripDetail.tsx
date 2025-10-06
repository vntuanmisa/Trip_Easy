import React from 'react';
import { useTranslation } from 'react-i18next';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { 
  ArrowLeftIcon,
  UserGroupIcon,
  CalendarDaysIcon,
  CurrencyDollarIcon,
  ShareIcon
} from '@heroicons/react/24/outline';
import { TripService } from '../services/tripService';
import { formatDate } from '../utils/dateUtils';
import { formatCurrency } from '../utils/currencyUtils';
import LoadingSpinner from '../components/LoadingSpinner';

const TripDetail: React.FC = () => {
  const { t, i18n } = useTranslation();
  const { tripId } = useParams<{ tripId: string }>();
  
  const { data: trip, isLoading, error } = useQuery({
    queryKey: ['trip', tripId],
    queryFn: () => TripService.getTrip(Number(tripId)),
    enabled: !!tripId,
  });

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error || !trip) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 mb-4">
          {t('error.notFound')}
        </div>
        <Link to="/" className="btn-primary">
          {t('common.back')}
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <Link
            to="/"
            className="mr-4 p-2 text-gray-600 hover:text-gray-900 transition-colors"
          >
            <ArrowLeftIcon className="h-6 w-6" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              {trip.name}
            </h1>
            <p className="text-sm text-gray-500">
              {trip.destination} • {formatDate(trip.start_date, 'dd/MM/yyyy', i18n.language)} - {formatDate(trip.end_date, 'dd/MM/yyyy', i18n.language)}
            </p>
          </div>
        </div>
        
        <button className="btn-outline flex items-center space-x-2">
          <ShareIcon className="h-5 w-5" />
          <span>{t('common.share')}</span>
        </button>
      </div>

      {/* Trip Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card text-center">
          <UserGroupIcon className="h-8 w-8 text-primary-600 mx-auto mb-2" />
          <h3 className="text-lg font-semibold text-gray-900">
            {trip.members?.length || 0}
          </h3>
          <p className="text-sm text-gray-600">{t('trip.members')}</p>
        </div>
        
        <div className="card text-center">
          <CalendarDaysIcon className="h-8 w-8 text-primary-600 mx-auto mb-2" />
          <h3 className="text-lg font-semibold text-gray-900">
            {trip.activities?.length || 0}
          </h3>
          <p className="text-sm text-gray-600">{t('trip.activities')}</p>
        </div>
        
        <div className="card text-center">
          <CurrencyDollarIcon className="h-8 w-8 text-primary-600 mx-auto mb-2" />
          <h3 className="text-lg font-semibold text-gray-900">
            {formatCurrency(0, trip.currency, i18n.language)}
          </h3>
          <p className="text-sm text-gray-600">{t('expense.total')}</p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <button className="card-hover text-center p-4">
          <UserGroupIcon className="h-6 w-6 text-primary-600 mx-auto mb-2" />
          <span className="text-sm font-medium">{t('trip.members')}</span>
        </button>
        
        <button className="card-hover text-center p-4">
          <CalendarDaysIcon className="h-6 w-6 text-primary-600 mx-auto mb-2" />
          <span className="text-sm font-medium">{t('trip.activities')}</span>
        </button>
        
        <button className="card-hover text-center p-4">
          <CurrencyDollarIcon className="h-6 w-6 text-primary-600 mx-auto mb-2" />
          <span className="text-sm font-medium">{t('trip.expenses')}</span>
        </button>
        
        <button className="card-hover text-center p-4">
          <ShareIcon className="h-6 w-6 text-primary-600 mx-auto mb-2" />
          <span className="text-sm font-medium">{t('trip.summary')}</span>
        </button>
      </div>

      {/* Trip Info */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Thông tin chuyến đi
        </h2>
        <div className="space-y-3">
          {trip.description && (
            <div>
              <h3 className="text-sm font-medium text-gray-700">Mô tả</h3>
              <p className="text-gray-600">{trip.description}</p>
            </div>
          )}
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 className="text-sm font-medium text-gray-700">Mã mời</h3>
              <div className="flex items-center justify-between bg-gray-50 rounded-lg px-3 py-2 mt-1">
                <span className="font-mono text-lg">{trip.invite_code}</span>
                <button className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                  {t('common.copy')}
                </button>
              </div>
            </div>
            
            <div>
              <h3 className="text-sm font-medium text-gray-700">Tiền tệ chính</h3>
              <p className="text-gray-600 mt-1">{t(`currency.${trip.currency}`)}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Placeholder for tabs content */}
      <div className="card">
        <div className="text-center py-8 text-gray-500">
          <p>Các tính năng khác đang được phát triển...</p>
          <p className="text-sm mt-2">Thành viên, Hoạt động, Chi phí, Báo cáo</p>
        </div>
      </div>
    </div>
  );
};

export default TripDetail;
