clear all; close all


data = load('pose_data_cam_pentagon_2000.txt');

shift = 20;

velx = data(:,1);
vely = data(:,2);

feed = 2/60;%m/sec
side = 0.2; %m

t = linspace(0, (0.8/feed), length(velx));

gtVx = t;
gtVy = t;
side_counts1 = 87;
side_counts2 = 63;
side_counts = 0;
flag = 1;
tap= 0;
for i=1:1:length(velx)-shift
    
    if flag ==2 || flag ==3
        side_counts =side_counts2;
    else
        side_counts =side_counts1;
    end

    if mod(i-tap,side_counts) == 0
        if flag >= 5
            flag = 0;
        end
        flag = flag+1;
        if flag == 2 || flag == 3 || flag == 4
            tap = i-1;
        end
    end
    
   if flag == 1
        gtVx(i+shift) = 0;
        gtVy(i+shift) = feed;
   elseif flag ==2
       gtVx(i+shift) = -feed/2^0.5;
       gtVy(i+shift) = feed/2^0.5;
   elseif flag ==3
       gtVx(i+shift) = -feed/2^0.5;
       gtVy(i+shift) = -feed/2^0.5;
   elseif flag ==4
       gtVx(i+shift) = 0;
       gtVy(i+shift) = -feed;
   elseif flag ==5
       gtVx(i+shift) = feed;
       gtVy(i+shift) = 0;
   end
%    side_counts
%    flag
end


gtVx(1:shift) = zeros(1,shift);
gtVy(1:shift) = zeros(1,shift);



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

velymf(shift+1:end) = circshift(velymf(shift+1:end), -70);
vely(shift+1:end) = circshift(vely(shift+1:end), -70);



scaleFactor = 5;
velxmf = velxmf/scaleFactor;
velymf = -velymf/scaleFactor;

writerObj = VideoWriter('pent.avi');
writerObj.FrameRate = 10;
open(writerObj);

figure
hold on
gtpx = 0;
gtpy = 0;
px = 0;
py = 0;
theta = -45;
theta = 0;
theta = theta*pi/180;
R = [cos(theta), -sin(theta); sin(theta), cos(theta)];
for i=1:1:length(velxmf)
    
    outv = R*[velxmf(i);velymf(i)];
    velxmf(i) = outv(1);
    velymf(i) = outv(2);
    
    px = px+velxmf(i)/10;
    py = py+velymf(i)/10;
    gtpx = gtpx+gtVx(i)/10;
    gtpy = gtpy+gtVy(i)/10;
    scatter(px, py,10,'b')
    scatter(gtpx, gtpy,10,'r')
    axis(0.1*[-10,10,-10,10])
    xlabel('X (m)')
    ylabel('Y (m)')
    legend('computed', 'CNC reference')
    F = getframe(gcf) ;
    writeVideo(writerObj, F);
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
title('Pentagon x')


figure
plot(t,vely,'b')
hold on
plot(t,-velymf*scaleFactor,'r')
xlabel('time (secs)')
ylabel('velocity (m/s)')
legend('y velocity unfiltered', 'y velocity median+butter')
title('Pentagon y')

figure
plot(t,gtVx,'b')
hold on
plot(t,velxmf,'r')
xlabel('time (secs)')
ylabel('velocity (m/s)')
legend('x velocity reference', 'x velocity computed')
title('Comparing velocities - X')

figure
plot(t,gtVy,'b')
hold on
plot(t,velymf,'r')
xlabel('time (secs)')
ylabel('velocity (m/s)')
legend('y velocity reference', 'y velocity computed')
title('Comparing velocities - Y')

%%%%%%%%%%%%%%%%%%%
% pos = zeros(4,length(velxmf));
% for i=1:1:length(velxmf)
%     
%     outv = R*[velxmf(i);velymf(i)];
%     velxmf(i) = outv(1);
%     velymf(i) = outv(2);
%     
%     px = px+velxmf(i)/10;
%     py = py+velymf(i)/10;
%     gtpx = gtpx+gtVx(i)/10;
%    gtpy = gtpy+gtVy(i)/10;
%     pos(1,i) = gtpx;
%     pos(2,i) = gtpy;
%     pos(3,i) = px;
%     pos(4,i) = py;
% end
% 
% 
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
% 
% figure
% plot(t,pos(3,:) - pos(1,:),'b')
% xlabel('time (secs)')
% ylabel('Position error (m)')
% title('Position error - X')
% figure
% plot(t,pos(4,:) - pos(2,:),'b')
% xlabel('time (secs)')
% ylabel('Position error (m)')
% title('Position error - Y')

