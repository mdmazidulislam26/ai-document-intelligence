/**
 * Exact decimal formatting and multiplication utilities for financial UI inputs.
 * Avoids IEEE-754 binary floating-point rounding drift (e.g. 0.1 + 0.2, 1.005.toFixed(2)).
 * Compatible with ES5 TypeScript target.
 */

function parseDecimalParts(val: string | number | null | undefined): {
  negative: boolean;
  digits: string;
  scale: number;
} | null {
  if (val === null || val === undefined || val === '') return null;
  const cleaned = String(val).trim().replace(/[^0-9.-]/g, '');
  if (!cleaned || cleaned === '-' || cleaned === '.') return null;

  const negative = cleaned.startsWith('-');
  const unsigned = negative ? cleaned.slice(1) : cleaned;
  const parts = unsigned.split('.');
  const intPart = (parts[0] || '0').replace(/\D/g, '') || '0';
  const fracPart = (parts[1] || '').replace(/\D/g, '');

  return {
    negative,
    digits: (intPart + fracPart).replace(/^0+(?=\d)/, '') || '0',
    scale: fracPart.length,
  };
}

export function formatMoney(val: string | number | null | undefined): string {
  const parsed = parseDecimalParts(val);
  if (!parsed) return '';

  const { negative, digits, scale } = parsed;
  const padded = digits.padStart(scale + 1, '0');
  const splitIdx = padded.length - scale;
  const intPart = padded.slice(0, splitIdx).replace(/^0+(?=\d)/, '') || '0';
  const fracRaw = padded.slice(splitIdx);

  const fracPadded = (fracRaw + '000').slice(0, 3);
  let cents = parseInt(fracPadded.slice(0, 2), 10);
  const thirdDigit = parseInt(fracPadded[2], 10);

  let carry = 0;
  if (thirdDigit >= 5) {
    cents += 1;
    if (cents >= 100) {
      cents = 0;
      carry = 1;
    }
  }

  let finalInt = intPart;
  if (carry === 1) {
    const arr = intPart.split('').map(Number);
    let c = 1;
    for (let i = arr.length - 1; i >= 0 && c > 0; i--) {
      const sum = arr[i] + c;
      arr[i] = sum % 10;
      c = Math.floor(sum / 10);
    }
    if (c > 0) arr.unshift(c);
    finalInt = arr.join('');
  }

  const centsStr = cents < 10 ? `0${cents}` : `${cents}`;
  const isZero = finalInt === '0' && centsStr === '00';
  return `${negative && !isZero ? '-' : ''}${finalInt}.${centsStr}`;
}

export function multiplyMoney(
  a: string | number | null | undefined,
  b: string | number | null | undefined
): string {
  const pa = parseDecimalParts(a);
  const pb = parseDecimalParts(b);
  if (!pa || !pb) return '0.00';

  const d1 = pa.digits.split('').reverse().map(Number);
  const d2 = pb.digits.split('').reverse().map(Number);
  const prod = new Array(d1.length + d2.length).fill(0);

  for (let i = 0; i < d1.length; i++) {
    for (let j = 0; j < d2.length; j++) {
      prod[i + j] += d1[i] * d2[j];
    }
  }

  for (let k = 0; k < prod.length - 1; k++) {
    prod[k + 1] += Math.floor(prod[k] / 10);
    prod[k] %= 10;
  }

  const rawDigits = prod.reverse().join('').replace(/^0+(?=\d)/, '') || '0';
  const totalScale = pa.scale + pb.scale;
  const negative = pa.negative !== pb.negative;

  const padded = rawDigits.padStart(totalScale + 1, '0');
  const decStr =
    totalScale > 0
      ? `${padded.slice(0, padded.length - totalScale)}.${padded.slice(padded.length - totalScale)}`
      : padded;

  return formatMoney(`${negative ? '-' : ''}${decStr}`);
}
