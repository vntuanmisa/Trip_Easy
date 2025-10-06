import React from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { ExclamationTriangleIcon, HomeIcon } from '@heroicons/react/24/outline';

const NotFound: React.FC = () => {
  const { t } = useTranslation();

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="max-w-md w-full text-center">
        <div className="mx-auto h-24 w-24 text-gray-400 mb-6">
          <ExclamationTriangleIcon className="h-full w-full" />
        </div>
        
        <h1 className="text-4xl font-bold text-gray-900 mb-4">404</h1>
        <h2 className="text-xl font-semibold text-gray-700 mb-4">
          {t('error.notFound')}
        </h2>
        <p className="text-gray-600 mb-8">
          Trang bạn đang tìm kiếm không tồn tại hoặc đã được di chuyển.
        </p>
        
        <Link
          to="/"
          className="btn-primary inline-flex items-center space-x-2"
        >
          <HomeIcon className="h-5 w-5" />
          <span>Về trang chủ</span>
        </Link>
      </div>
    </div>
  );
};

export default NotFound;
