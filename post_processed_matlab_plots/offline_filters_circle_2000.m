clear all; close all


data = load('pose_data_cam_circle_2000.txt');
shift = 30;
velx = data(:,1);
vely = data(:,2);

feed = 2/60;%m/sec
rad = 0.1; %m
f = 1/(2*pi*rad/feed); %Hz
t = linspace(0, 2/f, length(velx));

gtVx = feed*cos(2*pi*f*t);
gtVy = feed*sin(2*pi*f*t);

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
velxmf = velxmf/scaleFactor;
velymf = -velymf/scaleFactor;

figure
hold on
gtpx = 0;
gtpy = 0;
px = 0;
py = 0;
theta = -37;
% theta = 0;
theta = theta*pi/180;
R = [cos(theta), -sin(theta); sin(theta), cos(theta)];
pos = zeros(4,length(velxmf));
for i=1:1:length(velxmf)
    
    outv = R*[velxmf(i);velymf(i)];
    velxmf(i) = outv(1);
    velymf(i) = outv(2);
    
    px = px+velxmf(i)/10;
    py = py+velymf(i)/10;
    gtpx = gtpx+gtVx(i)/10;
    gtpy = gtpy+gtVy(i)/10;
%     scatter(px, py,10,'b')
%     scatter(gtpx, gtpy,10,'r')
    
    pos(1,i) = gtpx;
    pos(2,i) = gtpy;
    pos(3,i) = px;
    pos(4,i) = py;
%     scatter(px, py,10,'b')
%     scatter(gtpx, gtpy,10,'r')
%     legend('computed', 'CNC reference')
%     axis(0.1*[-10,10,-10,10])
%     xlabel('X (m)')
%     ylabel('Y (m)')
%     pause(0.00000001)
end
% 
% % figure
% % plot(t,velxmf*scaleFactor,'r')
% % hold on
% % plot(t,velx,'b')
% % xlabel('time (secs)')
% % ylabel('velocity (m/s)')
% % legend('x velocity median+butter', 'x velocity unfiltered')
% % title('Circle x')
% % 
% % 
% % figure
% % plot(t,vely,'b')
% % hold on
% % plot(t,-velymf*scaleFactor,'r')
% % xlabel('time (secs)')
% % ylabel('velocity (m/s)')
% % legend('y velocity unfiltered', 'y velocity median+butter')
% % title('Circle y')
% 
% figure
% plot(t,gtVx,'b')
% hold on
% plot(t,velxmf,'r')
% xlabel('time (secs)')
% ylabel('velocity (m/s)')
% legend('x velocity reference', 'x velocity computed')
% title('Comparing velocities - X')
% 
% figure
% plot(t,gtVy,'b')
% hold on
figure
plot(t,pos(3,:) - pos(1,:),'b')
xlabel('time (secs)')
ylabel('Position error (m)')
title('Position error - X')
figure
plot(t,pos(4,:) - pos(2,:),'b')
xlabel('time (secs)')
ylabel('Position error (m)')
title('Position error - Y')

% plot(t,velymf,'r')
% xlabel('time (secs)')
% ylabel('velocity (m/s)')
% legend('y velocity reference', 'y velocity computed')
% title('Comparing velocities - Y')
% 
% figure
% plot(t,velxmf' - gtVx,'b')
% xlabel('time (secs)')
% ylabel('velocity error (m/s)')
% title('Velocity error - X')
% 
% figure
% plot(t,velymf' - gtVy,'b')
% xlabel('time (secs)')
% ylabel('velocity error (m/s)')
% title('Velocity error - Y')
% % 
% % 
