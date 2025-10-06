import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate, useParams } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { useMutation, useQuery } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { 
  ArrowLeftIcon,
  UserPlusIcon,
  QrCodeIcon
} from '@heroicons/react/24/outline';
import { TripService } from '../services/tripService';
import { MemberService } from '../services/memberService';
import { TripMemberCreate } from '../types';
import LoadingSpinner from '../components/LoadingSpinner';

const JoinTrip: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { inviteCode: urlInviteCode } = useParams();
  const [inviteCode, setInviteCode] = useState(urlInviteCode || '');
  const [step, setStep] = useState<'code' | 'member'>('code');
  
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<TripMemberCreate>({
    defaultValues: {
      factor: 1.0,
    },
  });

  // Get trip by invite code
  const { data: trip, isLoading: isLoadingTrip, error: tripError } = useQuery({
    queryKey: ['trip', 'invite', inviteCode],
    queryFn: () => TripService.getTripByInviteCode(inviteCode),
    enabled: !!inviteCode && step === 'member',
  });

  // Join trip mutation
  const joinTripMutation = useMutation({
    mutationFn: (data: { tripId: number; memberData: TripMemberCreate }) =>
      MemberService.joinTrip(data.tripId, data.memberData),
    onSuccess: (member) => {
      toast.success(t('success.memberAdded'));
      navigate(`/trips/${member.trip_id}`);
    },
    onError: (error: any) => {
      toast.error(error.detail || t('error.general'));
    },
  });

  const handleCodeSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inviteCode.trim()) {
      toast.error('Vui lòng nhập mã mời');
      return;
    }
    setStep('member');
  };

  const onSubmit = (data: TripMemberCreate) => {
    if (!trip) return;
    joinTripMutation.mutate({
      tripId: trip.id,
      memberData: data,
    });
  };

  if (step === 'code') {
    return (
      <div className="max-w-md mx-auto">
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
              {t('trip.join')}
            </h1>
            <p className="text-sm text-gray-500">
              Nhập mã mời để tham gia chuyến đi
            </p>
          </div>
        </div>

        {/* Code Form */}
        <div className="card">
          <div className="text-center mb-6">
            <div className="mx-auto h-16 w-16 bg-primary-100 rounded-full flex items-center justify-center mb-4">
              <QrCodeIcon className="h-8 w-8 text-primary-600" />
            </div>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">
              Mã mời chuyến đi
            </h2>
            <p className="text-sm text-gray-600">
              Nhập mã mời 8 ký tự mà bạn nhận được từ người tổ chức
            </p>
          </div>

          <form onSubmit={handleCodeSubmit} className="space-y-4">
            <div>
              <label htmlFor="inviteCode" className="block text-sm font-medium text-gray-700 mb-1">
                Mã mời <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                value={inviteCode}
                onChange={(e) => setInviteCode(e.target.value.toUpperCase())}
                className="input-field text-center text-lg font-mono tracking-wider"
                placeholder="XXXXXXXX"
                maxLength={8}
                required
              />
            </div>

            <button
              type="submit"
              className="btn-primary w-full"
            >
              Tiếp tục
            </button>
          </form>
        </div>
      </div>
    );
  }

  if (isLoadingTrip) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (tripError || !trip) {
    return (
      <div className="max-w-md mx-auto">
        <div className="card text-center">
          <div className="text-red-600 mb-4">
            <h2 className="text-lg font-semibold mb-2">Mã mời không hợp lệ</h2>
            <p className="text-sm">
              Mã mời này không tồn tại hoặc đã hết hạn. Vui lòng kiểm tra lại.
            </p>
          </div>
          <button
            onClick={() => setStep('code')}
            className="btn-primary"
          >
            Thử lại
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      {/* Header */}
      <div className="flex items-center mb-6">
        <button
          onClick={() => setStep('code')}
          className="mr-4 p-2 text-gray-600 hover:text-gray-900 transition-colors"
        >
          <ArrowLeftIcon className="h-6 w-6" />
        </button>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Tham gia chuyến đi
          </h1>
          <p className="text-sm text-gray-500">
            {trip.name} - {trip.destination}
          </p>
        </div>
      </div>

      {/* Trip Info */}
      <div className="card mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Thông tin chuyến đi
        </h2>
        <div className="space-y-2">
          <div className="flex justify-between">
            <span className="text-gray-600">Tên chuyến đi:</span>
            <span className="font-medium">{trip.name}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Điểm đến:</span>
            <span className="font-medium">{trip.destination}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Thời gian:</span>
            <span className="font-medium">
              {new Date(trip.start_date).toLocaleDateString('vi-VN')} - {new Date(trip.end_date).toLocaleDateString('vi-VN')}
            </span>
          </div>
        </div>
      </div>

      {/* Member Form */}
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <UserPlusIcon className="h-5 w-5 mr-2 text-primary-600" />
            Thông tin của bạn
          </h2>
          
          <div className="space-y-4">
            {/* Name */}
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                {t('member.name')} <span className="text-red-500">*</span>
              </label>
              <input
                {...register('name', { 
                  required: t('validation.required'),
                  minLength: { value: 2, message: t('validation.minLength', { min: 2 }) }
                })}
                type="text"
                className="input-field"
                placeholder="Nhập tên của bạn..."
              />
              {errors.name && (
                <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
              )}
            </div>

            {/* Email */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                {t('member.email')} <span className="text-gray-400">({t('common.optional')})</span>
              </label>
              <input
                {...register('email', {
                  pattern: {
                    value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                    message: t('validation.email')
                  }
                })}
                type="email"
                className="input-field"
                placeholder="email@example.com"
              />
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
              )}
            </div>

            {/* Factor */}
            <div>
              <label htmlFor="factor" className="block text-sm font-medium text-gray-700 mb-1">
                {t('member.factor')}
              </label>
              <select
                {...register('factor', { valueAsNumber: true })}
                className="input-field"
              >
                <option value={1.0}>Người lớn (1.0)</option>
                <option value={0.5}>Trẻ em (0.5)</option>
                <option value={0.7}>Học sinh (0.7)</option>
                <option value={1.5}>Tùy chỉnh (1.5)</option>
              </select>
              <p className="mt-1 text-xs text-gray-500">
                Hệ số này ảnh hưởng đến cách chia chi phí chung
              </p>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row sm:justify-end space-y-3 sm:space-y-0 sm:space-x-3">
          <button
            type="button"
            onClick={() => setStep('code')}
            className="btn-secondary"
          >
            {t('common.back')}
          </button>
          <button
            type="submit"
            disabled={joinTripMutation.isPending}
            className="btn-primary flex items-center justify-center space-x-2"
          >
            {joinTripMutation.isPending ? (
              <LoadingSpinner size="sm" />
            ) : (
              <>
                <UserPlusIcon className="h-5 w-5" />
                <span>Tham gia chuyến đi</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default JoinTrip;
