import { useState, useEffect } from 'react';
import apiClient from './apiClient';

export interface Expense {
  id: number;
  item: string;
  amount: number;
  category: string;
  date: string;
  created_by: string;
}

export interface MetricsSummary {
  daily: number;
  monthly: number;
  all_time: number;
}

export interface CategoryMetric {
  category: string;
  total: number;
}

export interface TrendData {
  date: string;
  total: number;
}

export interface Budget {
  id: string;
  category: string;
  limit_amount: number;
  period: 'monthly' | 'yearly';
  spent?: number;
}

// Hook to fetch expenses
export const useExpenses = (page = 1, limit = 20) => {
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    const fetchExpenses = async () => {
      try {
        setLoading(true);
        const response = await apiClient.get('/expenses', {
          params: { page, limit },
        });
        setExpenses(response.data.data.items || []);
        setTotal(response.data.data.total || 0);
        setError(null);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchExpenses();
  }, [page, limit]);

  return { expenses, loading, error, total };
};

// Hook to fetch metrics summary
export const useMetricsSummary = () => {
  const [metrics, setMetrics] = useState<MetricsSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        setLoading(true);
        const response = await apiClient.get('/metrics/summary');
        setMetrics(response.data.data);
        setError(null);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();
  }, []);

  return { metrics, loading, error };
};

// Hook to fetch category metrics
export const useCategoryMetrics = () => {
  const [categories, setCategories] = useState<CategoryMetric[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        setLoading(true);
        const response = await apiClient.get('/metrics/categories');
        setCategories(response.data.data.categories || []);
        setError(null);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, []);

  return { categories, loading, error };
};

// Hook to fetch trends
export const useTrends = () => {
  const [trends, setTrends] = useState<TrendData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTrends = async () => {
      try {
        setLoading(true);
        const response = await apiClient.get('/metrics/trends');
        setTrends(response.data.data.trends || []);
        setError(null);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchTrends();
  }, []);

  return { trends, loading, error };
};

// Hook to fetch budgets
export const useBudgets = () => {
  const [budgets, setBudgets] = useState<Budget[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchBudgets = async () => {
      try {
        setLoading(true);
        const response = await apiClient.get('/budgets');
        setBudgets(response.data.data.items || []);
        setError(null);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchBudgets();
  }, []);

  return { budgets, loading, error };
};
