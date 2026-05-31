export interface User {
  id: number;
  email: string;
}

export interface Expense {
  id: number;
  amount: number;
  category: string;
  description: string | null;
}

export interface TokenPair {
  access_token: string;
  refresh_token: string;
  token_type: string;
}
