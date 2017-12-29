%% Thomas Koch
% a script used to calculate the resistance values for a 4th order high pass
% butterworth filter, sallen key topology
% assumes capacitances are given

clc; clear all; close all;

c1 = .01e-6;
r3 = 10e3;
w_o = 2 * pi * 10e3;
alpha = 1.8478;

c2 = c1;
k = w_o * c1;

r1 = alpha / (2 * k)
r2 = 1 / (w_o^2 * r1 * c1^2)

omega = logspace(1,5,10000);
s = 1i * omega;

a_v1 = s.^2 ./ (s.^2 + alpha * w_o * s + w_o^2);


c1 = 1e-9;
r3 = 10e3;
alpha = .7654;

c2 = c1;
k = w_o * c1;

r1 = alpha / (2 * k)
r2 = 1 / (w_o^2 * r1 * c1^2)

alpha = 2 / (w_o * r2 * c1);

a_v2 = s.^2 ./ (s.^2 + alpha * w_o * s + w_o^2);


a_v = a_v1 .* a_v2;

figure;
plot(omega,20*log10(abs(a_v)));
