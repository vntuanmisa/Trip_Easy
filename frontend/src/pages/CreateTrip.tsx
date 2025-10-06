import React from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { useMutation } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { 
  ArrowLeftIcon,
  CalendarDaysIcon,
  MapPinIcon,
  CurrencyDollarIcon
} from '@heroicons/react/24/outline';
import { TripService } from '../services/tripService';
import { TripCreate, CurrencyEnum } from '../types';
import { formatDateForInput } from '../utils/dateUtils';
import LoadingSpinner from '../components/LoadingSpinner';

const CreateTrip: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm<TripCreate>({
    defaultValues: {
      currency: CurrencyEnum.VND,
      child_factor: 0.5,
      rounding_rule: 1000,
    },
  });

  const startDate = watch('start_date');

  const createTripMutation = useMutation({
    mutationFn: TripService.createTrip,
    onSuccess: (trip) => {
      toast.success(t('success.tripCreated'));
      navigate(`/trips/${trip.id}`);
    },
    onError: (error: any) => {
      toast.error(error.detail || t('error.general'));
    },
  });

  const onSubmit = (data: TripCreate) => {
    // Validate dates
    const start = new Date(data.start_date);
    const end = new Date(data.end_date);
    
    if (start >= end) {
      toast.error(t('validation.dateRange'));
      return;
    }
    
    if (start < new Date()) {
      toast.error(t('validation.pastDate'));
      return;
    }

    createTripMutation.mutate(data);
  };

  return (
    <div className="max-w-2xl mx-auto">
      {/* Header */}
      <div className="flex items-center mb-6">
        <button
          onClick={() => navigate(-1)}
          className="mr-4 p-2 text-gray-600 hover:text-gray-900 transition-colors"
        >
          <ArrowLeftIcon className="h-6 w-6" />
        </button>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {t('trip.create')}
          </h1>
          <p className="text-sm text-gray-500">
            Tạo chuyến đi mới và mời bạn bè tham gia
          </p>
        </div>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <MapPinIcon className="h-5 w-5 mr-2 text-primary-600" />
            Thông tin cơ bản
          </h2>
          
          <div className="space-y-4">
            {/* Trip Name */}
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                {t('trip.name')} <span className="text-red-500">*</span>
              </label>
              <input
                {...register('name', { 
                  required: t('validation.required'),
                  minLength: { value: 3, message: t('validation.minLength', { min: 3 }) }
                })}
                type="text"
                className="input-field"
                placeholder="Nhập tên chuyến đi..."
              />
              {errors.name && (
                <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
              )}
            </div>

            {/* Description */}
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                {t('trip.description')} <span className="text-gray-400">({t('common.optional')})</span>
              </label>
              <textarea
                {...register('description')}
                rows={3}
                className="input-field resize-none"
                placeholder="Mô tả về chuyến đi..."
              />
            </div>

            {/* Destination */}
            <div>
              <label htmlFor="destination" className="block text-sm font-medium text-gray-700 mb-1">
                {t('trip.destination')} <span className="text-red-500">*</span>
              </label>
              <input
                {...register('destination', { 
                  required: t('validation.required'),
                  minLength: { value: 2, message: t('validation.minLength', { min: 2 }) }
                })}
                type="text"
                className="input-field"
                placeholder="Nhập điểm đến..."
              />
              {errors.destination && (
                <p className="mt-1 text-sm text-red-600">{errors.destination.message}</p>
              )}
            </div>
          </div>
        </div>

        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <CalendarDaysIcon className="h-5 w-5 mr-2 text-primary-600" />
            Thời gian
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Start Date */}
            <div>
              <label htmlFor="start_date" className="block text-sm font-medium text-gray-700 mb-1">
                {t('trip.startDate')} <span className="text-red-500">*</span>
              </label>
              <input
                {...register('start_date', { required: t('validation.required') })}
                type="datetime-local"
                className="input-field"
                min={formatDateForInput(new Date())}
              />
              {errors.start_date && (
                <p className="mt-1 text-sm text-red-600">{errors.start_date.message}</p>
              )}
            </div>

            {/* End Date */}
            <div>
              <label htmlFor="end_date" className="block text-sm font-medium text-gray-700 mb-1">
                {t('trip.endDate')} <span className="text-red-500">*</span>
              </label>
              <input
                {...register('end_date', { required: t('validation.required') })}
                type="datetime-local"
                className="input-field"
                min={startDate || formatDateForInput(new Date())}
              />
              {errors.end_date && (
                <p className="mt-1 text-sm text-red-600">{errors.end_date.message}</p>
              )}
            </div>
          </div>
        </div>

        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <CurrencyDollarIcon className="h-5 w-5 mr-2 text-primary-600" />
            Cài đặt tài chính
          </h2>
          
          <div className="space-y-4">
            {/* Currency */}
            <div>
              <label htmlFor="currency" className="block text-sm font-medium text-gray-700 mb-1">
                {t('trip.currency')}
              </label>
              <select
                {...register('currency')}
                className="input-field"
              >
                <option value={CurrencyEnum.VND}>{t('currency.VND')}</option>
                <option value={CurrencyEnum.USD}>{t('currency.USD')}</option>
                <option value={CurrencyEnum.EUR}>{t('currency.EUR')}</option>
                <option value={CurrencyEnum.JPY}>{t('currency.JPY')}</option>
                <option value={CurrencyEnum.KRW}>{t('currency.KRW')}</option>
                <option value={CurrencyEnum.THB}>{t('currency.THB')}</option>
              </select>
            </div>

            {/* Child Factor */}
            <div>
              <label htmlFor="child_factor" className="block text-sm font-medium text-gray-700 mb-1">
                Hệ số chi tiêu trẻ em (so với người lớn)
              </label>
              <input
                {...register('child_factor', { 
                  valueAsNumber: true,
                  min: { value: 0, message: t('validation.positiveNumber') },
                  max: { value: 2, message: 'Tối đa 2.0' }
                })}
                type="number"
                step="0.1"
                min="0"
                max="2"
                className="input-field"
              />
              <p className="mt-1 text-xs text-gray-500">
                Ví dụ: 0.5 nghĩa là trẻ em chỉ tính 50% chi phí của người lớn
              </p>
            </div>

            {/* Rounding Rule */}
            <div>
              <label htmlFor="rounding_rule" className="block text-sm font-medium text-gray-700 mb-1">
                Quy tắc làm tròn (VND)
              </label>
              <select
                {...register('rounding_rule', { valueAsNumber: true })}
                className="input-field"
              >
                <option value={1}>Không làm tròn</option>
                <option value={100}>Làm tròn đến hàng trăm</option>
                <option value={1000}>Làm tròn đến hàng nghìn</option>
                <option value={10000}>Làm tròn đến hàng vạn</option>
              </select>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row sm:justify-end space-y-3 sm:space-y-0 sm:space-x-3">
          <button
            type="button"
            onClick={() => navigate(-1)}
            className="btn-secondary"
          >
            {t('common.cancel')}
          </button>
          <button
            type="submit"
            disabled={createTripMutation.isPending}
            className="btn-primary flex items-center justify-center space-x-2"
          >
            {createTripMutation.isPending ? (
              <LoadingSpinner size="sm" />
            ) : (
              <>
                <span>{t('common.create')}</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreateTrip;