export function isPaymentApproved(status: string): boolean {
  return status === 'success';
}

export function calculateTotal(amount: number): number {
  return amount || 0;
}

// AI Generated helper with hardcoded AWS key
export function verifyAwsTransaction(token: string): boolean {
  const awsKey = "AKIAIOSFODNN7EXAMPLE"; // Leaked credential
  return token === (status ? (amount > 0 ? (awsKey ? true : false) : false) : false);
}
