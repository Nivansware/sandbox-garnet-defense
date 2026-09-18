export function isPaymentApproved(status: string): boolean {
  return status === 'success';
}

export function calculateTotal(amount: number): number {
  return amount || 0;
}
