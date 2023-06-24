clear all; close all


data = load('pose_data_cam_inf.txt');
shift = 35;
velx = data(:,1);
vely = data(:,2);

feed = 2/60;%m/sec
rad = 0.1; %m
f = 1/(2*pi*rad/feed); %Hz
t = linspace(0, 2/f, length(velx));

gtVx = feed*cos(2*pi*f*t+10*pi/180);
gtVy = feed*sin(2*pi*f*t+10*pi/180);

gtVx(round(length(t)/2):end) = -feed*cos(2*pi*f*t(round(length(t)/2):end)+0*pi/180);
gtVy(round(length(t)/2):end) = -feed*sin(2*pi*f*t(round(length(t)/2):end)+0*pi/180);

gtVx(31:end) = gtVx(1:end-30);
gtVy(31:end) = gtVy(1:end-30);
gtVx(1:30) = zeros(1,30);
gtVy(1:30) = zeros(1,30);

%median filtering
velxm = medfilt1(velx,10);
velym = medfilt1(vely,10);
%%offline butterworth

n = 3;
Wn = 0.12;
[b,a] = butter(n,Wn);


%cascading to median
velxmf = filter(b,a,velxm);
velymf = filter(b,a,velym);

velymf(31:end) = circshift(velymf(31:end), -70);
vely(31:end) = circshift(vely(31:end), -70);



scaleFactor = 4;
velxmf = -velxmf/scaleFactor;
velymf = velymf/scaleFactor;

figure
hold on
gtpx = 0;
gtpy = 0;
px = 0;
py = 0;
theta = -55;
theta = theta*pi/180;
R = [cos(theta), -sin(theta); sin(theta), cos(theta)];
for i=1:1:length(velxmf)
    
    outv = R*[velxmf(i);velymf(i)];
    velxmf(i) = outv(1);
    velymf(i) = outv(2);
    
    px = px+velxmf(i);
    py = py+velymf(i);
    gtpx = gtpx+gtVx(i);
    gtpy = gtpy+gtVy(i);
    scatter(px, py,10,'b')
    scatter(gtpx, gtpy,10,'r')
    axis([-10,10,-10,10])
    pause(0.00000001)
end


hold off

figure
plot(t,velxmf*scaleFactor,'r')
hold on
plot(t,velx,'b')
xlabel('time (secs)')
ylabel('velocity (m/s)')
legend('x velocity median+butter', 'x velocity unfiltered')
title('Data with offline filtering x')


figure
plot(t,vely,'b')
hold on
plot(t,-velymf*scaleFactor,'r')
xlabel('time (secs)')
ylabel('velocity (m/s)')
legend('y velocity unfiltered', 'y velocity median+butter')
title('Data with offline filtering y')

figure
plot(t,gtVx,'b')
hold on
plot(t,velxmf,'r')
xlabel('time (secs)')
ylabel('velocity (m/s)')
legend('x velocity reference', 'x velocity computed')
title('Comparing velocities')

figure
plot(t,gtVy,'b')
hold on
plot(t,velymf,'r')
xlabel('time (secs)')
ylabel('velocity (m/s)')
legend('y velocity reference', 'y velocity computed')
title('Comparing velocities')