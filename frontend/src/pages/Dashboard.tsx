import React from 'react';
import { useTranslation } from 'react-i18next';
import { 
  PlusIcon, 
  UserGroupIcon, 
  CalendarDaysIcon, 
  CurrencyDollarIcon,
  MapPinIcon 
} from '@heroicons/react/24/outline';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { TripService } from '../services/tripService';
import { Trip } from '../types';
import { formatDate, getRelativeDate } from '../utils/dateUtils';
import { formatCurrency } from '../utils/currencyUtils';
import LoadingSpinner from '../components/LoadingSpinner';

const Dashboard: React.FC = () => {
  const { t, i18n } = useTranslation();

  const { data: trips = [], isLoading, error } = useQuery({
    queryKey: ['trips'],
    queryFn: () => TripService.getTrips(),
  });

  const getStatusColor = (trip: Trip) => {
    const now = new Date();
    const startDate = new Date(trip.start_date);
    const endDate = new Date(trip.end_date);

    if (now < startDate) return 'bg-blue-100 text-blue-800';
    if (now >= startDate && now <= endDate) return 'bg-green-100 text-green-800';
    return 'bg-gray-100 text-gray-800';
  };

  const getStatusText = (trip: Trip) => {
    const now = new Date();
    const startDate = new Date(trip.start_date);
    const endDate = new Date(trip.end_date);

    if (now < startDate) return t('trip.upcoming');
    if (now >= startDate && now <= endDate) return t('trip.ongoing');
    return t('trip.completed');
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 mb-4">
          {t('error.general')}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {t('navigation.dashboard')}
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Quản lý các chuyến đi của bạn
          </p>
        </div>
        
        <div className="mt-4 sm:mt-0 flex space-x-3">
          <Link
            to="/trips/join"
            className="btn-outline"
          >
            {t('trip.join')}
          </Link>
          <Link
            to="/trips/create"
            className="btn-primary flex items-center space-x-2"
          >
            <PlusIcon className="h-5 w-5" />
            <span>{t('trip.create')}</span>
          </Link>
        </div>
      </div>

      {/* Trips Grid */}
      {trips.length === 0 ? (
        <div className="text-center py-12">
          <div className="mx-auto h-24 w-24 text-gray-400 mb-4">
            <MapPinIcon className="h-full w-full" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            {t('trip.noTrips')}
          </h3>
          <p className="text-gray-500 mb-6">
            {t('trip.createFirstTrip')}
          </p>
          <Link
            to="/trips/create"
            className="btn-primary inline-flex items-center space-x-2"
          >
            <PlusIcon className="h-5 w-5" />
            <span>{t('trip.create')}</span>
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {trips.map((trip) => (
            <Link
              key={trip.id}
              to={`/trips/${trip.id}`}
              className="card-hover group"
            >
              {/* Status Badge */}
              <div className="flex justify-between items-start mb-3">
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(trip)}`}>
                  {getStatusText(trip)}
                </span>
                <div className="text-right">
                  <p className="text-sm text-gray-500">
                    {getRelativeDate(trip.start_date, i18n.language)}
                  </p>
                </div>
              </div>

              {/* Trip Info */}
              <div className="mb-4">
                <h3 className="text-lg font-semibold text-gray-900 group-hover:text-primary-600 transition-colors mb-1">
                  {trip.name}
                </h3>
                <div className="flex items-center text-sm text-gray-600 mb-2">
                  <MapPinIcon className="h-4 w-4 mr-1" />
                  {trip.destination}
                </div>
                <p className="text-sm text-gray-500">
                  {formatDate(trip.start_date, 'dd/MM/yyyy', i18n.language)} - {formatDate(trip.end_date, 'dd/MM/yyyy', i18n.language)}
                </p>
              </div>

              {/* Trip Stats */}
              <div className="grid grid-cols-3 gap-4 pt-4 border-t border-gray-200">
                <div className="text-center">
                  <UserGroupIcon className="h-5 w-5 text-gray-400 mx-auto mb-1" />
                  <p className="text-xs text-gray-500">{t('trip.members')}</p>
                  <p className="text-sm font-medium text-gray-900">-</p>
                </div>
                <div className="text-center">
                  <CalendarDaysIcon className="h-5 w-5 text-gray-400 mx-auto mb-1" />
                  <p className="text-xs text-gray-500">{t('trip.activities')}</p>
                  <p className="text-sm font-medium text-gray-900">-</p>
                </div>
                <div className="text-center">
                  <CurrencyDollarIcon className="h-5 w-5 text-gray-400 mx-auto mb-1" />
                  <p className="text-xs text-gray-500">{t('expense.total')}</p>
                  <p className="text-sm font-medium text-gray-900">-</p>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
