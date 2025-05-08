import React, { useState } from 'react';
import {
  FemelColors,
  FemelButton,
  FemelInput,
  FemelCard,
  FemelBadge,
  FemelTag,
  FemelProgress,
  FemelRadio,
  FemelCheckbox,
  FemelAlert,
  FemelSpinner,
  FemelDatePicker,
  FemelSwitch
} from '../components/FemelUI';

const FemelDemo = () => {
  const [inputValue, setInputValue] = useState('');
  const [dateValue, setDateValue] = useState('');
  const [switchChecked, setSwitchChecked] = useState(false);
  const [radioOption, setRadioOption] = useState('monthly');
  const [reminderChecked, setReminderChecked] = useState(true);
  const [privacyChecked, setPrivacyChecked] = useState(false);
  
  return (
    <div className="femel-demo-container" style={{ padding: '40px', backgroundColor: FemelColors.background }}>
      <h1 style={{ color: FemelColors.text, marginBottom: '40px', textAlign: 'center' }}>女性健康系统UI组件</h1>
      
      {/* 颜色展示 */}
      <FemelCard title="颜色方案">
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px' }}>
          {Object.entries(FemelColors).map(([name, color]) => (
            <div key={name} style={{ textAlign: 'center' }}>
              <div 
                style={{ 
                  width: '80px', 
                  height: '80px', 
                  backgroundColor: color, 
                  borderRadius: '12px',
                  boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
                  marginBottom: '8px'
                }} 
              />
              <div style={{ fontSize: '14px', color: FemelColors.text }}>{name}</div>
              <div style={{ fontSize: '12px', color: '#777' }}>{color}</div>
            </div>
          ))}
        </div>
      </FemelCard>
      
      {/* 按钮展示 */}
      <FemelCard title="按钮设计">
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px', marginBottom: '24px' }}>
          <FemelButton type="primary">主要按钮</FemelButton>
          <FemelButton type="secondary">次要按钮</FemelButton>
          <FemelButton type="outline">轮廓按钮</FemelButton>
          <FemelButton type="text">文本按钮</FemelButton>
          <FemelButton type="primary" disabled>禁用按钮</FemelButton>
        </div>
        
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px' }}>
          <FemelButton type="primary" size="small">小按钮</FemelButton>
          <FemelButton type="primary" size="medium">中按钮</FemelButton>
          <FemelButton type="primary" size="large">大按钮</FemelButton>
        </div>
      </FemelCard>
      
      {/* 输入框展示 */}
      <FemelCard title="输入框设计">
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <FemelInput 
            placeholder="请输入姓名" 
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
          />
          
          <FemelInput 
            placeholder="请输入邮箱" 
            type="email"
            icon={<span>✉️</span>}
          />
          
          <FemelInput 
            placeholder="请输入密码" 
            type="password"
            error="密码长度至少为8位"
          />
          
          <FemelInput 
            placeholder="禁用状态" 
            disabled
          />
        </div>
      </FemelCard>
      
      {/* 标签和徽章展示 */}
      <FemelCard title="标签与徽章">
        <div style={{ marginBottom: '24px' }}>
          <h4 style={{ marginBottom: '12px', color: FemelColors.text }}>标签</h4>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            <FemelTag text="健康记录" variant="primary" />
            <FemelTag text="生理周期" variant="secondary" />
            <FemelTag text="健身计划" variant="success" />
            <FemelTag text="待办事项" variant="warning" />
            <FemelTag text="重要提醒" variant="error" />
            <FemelTag text="可关闭标签" variant="primary" onClose={() => alert('标签关闭')} />
          </div>
        </div>
        
        <div>
          <h4 style={{ marginBottom: '12px', color: FemelColors.text }}>徽章</h4>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px', alignItems: 'center' }}>
            <FemelBadge count={5} variant="primary" />
            <FemelBadge count={10} variant="secondary" />
            <FemelBadge count={15} variant="success" />
            <FemelBadge count={20} variant="warning" />
            <FemelBadge count={99} variant="error" />
            <span style={{ position: 'relative', marginLeft: '8px' }}>
              消息通知
              <span style={{ position: 'absolute', top: '-5px', right: '-12px' }}>
                <FemelBadge dot variant="primary" />
              </span>
            </span>
          </div>
        </div>
      </FemelCard>
      
      {/* 进度指示器展示 */}
      <FemelCard title="进度指示器">
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div>
            <h4 style={{ marginBottom: '12px', color: FemelColors.text }}>小尺寸</h4>
            <FemelProgress percent={25} size="small" />
          </div>
          
          <div>
            <h4 style={{ marginBottom: '12px', color: FemelColors.text }}>默认尺寸</h4>
            <FemelProgress percent={50} />
          </div>
          
          <div>
            <h4 style={{ marginBottom: '12px', color: FemelColors.text }}>大尺寸</h4>
            <FemelProgress percent={75} size="large" />
          </div>
        </div>
      </FemelCard>
      
      {/* 单选和复选框展示 */}
      <FemelCard title="单选与复选框">
        <div style={{ display: 'flex', gap: '48px' }}>
          <div>
            <h4 style={{ marginBottom: '16px', color: FemelColors.text }}>生理周期记录</h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <FemelRadio 
                label="按月记录" 
                name="cycleType"
                checked={radioOption === 'monthly'} 
                onChange={() => setRadioOption('monthly')} 
              />
              <FemelRadio 
                label="按周记录" 
                name="cycleType"
                checked={radioOption === 'weekly'} 
                onChange={() => setRadioOption('weekly')} 
              />
              <FemelRadio 
                label="自定义" 
                name="cycleType"
                checked={radioOption === 'custom'} 
                onChange={() => setRadioOption('custom')} 
              />
            </div>
          </div>
          
          <div>
            <h4 style={{ marginBottom: '16px', color: FemelColors.text }}>选项设置</h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <FemelCheckbox 
                label="接收提醒通知" 
                checked={reminderChecked} 
                onChange={() => setReminderChecked(!reminderChecked)} 
              />
              <FemelCheckbox 
                label="同意隐私条款" 
                checked={privacyChecked} 
                onChange={() => setPrivacyChecked(!privacyChecked)} 
              />
            </div>
          </div>
        </div>
      </FemelCard>
      
      {/* 提示框展示 */}
      <FemelCard title="提示框">
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <FemelAlert message="这是一条普通信息提示" type="info" onClose={() => alert('关闭提示')} />
          <FemelAlert message="操作已成功完成" type="success" onClose={() => alert('关闭提示')} />
          <FemelAlert message="请注意此操作可能有风险" type="warning" onClose={() => alert('关闭提示')} />
          <FemelAlert message="操作失败，请重试" type="error" onClose={() => alert('关闭提示')} />
        </div>
      </FemelCard>
      
      {/* 加载中、日期选择器和开关展示 */}
      <FemelCard title="其他组件">
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '48px' }}>
          <div>
            <h4 style={{ marginBottom: '16px', color: FemelColors.text }}>加载中</h4>
            <div style={{ display: 'flex', gap: '24px', alignItems: 'center' }}>
              <FemelSpinner size="small" />
              <FemelSpinner size="medium" />
              <FemelSpinner size="large" />
            </div>
          </div>
          
          <div>
            <h4 style={{ marginBottom: '16px', color: FemelColors.text }}>日期选择器</h4>
            <FemelDatePicker 
              placeholder="选择日期" 
              value={dateValue}
              onChange={(e) => setDateValue(e.target.value)}
            />
          </div>
          
          <div>
            <h4 style={{ marginBottom: '16px', color: FemelColors.text }}>开关</h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <FemelSwitch 
                  checked={switchChecked} 
                  onChange={() => setSwitchChecked(!switchChecked)}
                  size="small"
                />
                <span>小尺寸</span>
              </div>
              
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <FemelSwitch 
                  checked={switchChecked} 
                  onChange={() => setSwitchChecked(!switchChecked)}
                />
                <span>默认尺寸</span>
              </div>
              
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <FemelSwitch 
                  checked={switchChecked} 
                  onChange={() => setSwitchChecked(!switchChecked)}
                  size="large"
                />
                <span>大尺寸</span>
              </div>
            </div>
          </div>
        </div>
      </FemelCard>
      
      {/* 示例卡片 */}
      <FemelCard title="健康记录统计" variant="soft">
        <div style={{ padding: '16px 0' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '24px' }}>
            <div>
              <h4 style={{ color: FemelColors.text, marginBottom: '8px' }}>本月健康评分</h4>
              <div style={{ display: 'flex', alignItems: 'center' }}>
                <span style={{ fontSize: '32px', fontWeight: 'bold', color: FemelColors.primary }}>86</span>
                <span style={{ marginLeft: '8px', color: FemelColors.success }}>↑4%</span>
              </div>
            </div>
            
            <div>
              <h4 style={{ color: FemelColors.text, marginBottom: '8px' }}>完成度</h4>
              <div style={{ fontSize: '32px', fontWeight: 'bold', color: FemelColors.accent }}>75%</div>
            </div>
            
            <div>
              <h4 style={{ color: FemelColors.text, marginBottom: '8px' }}>目标达成</h4>
              <div style={{ fontSize: '32px', fontWeight: 'bold', color: FemelColors.success }}>12/15</div>
            </div>
          </div>
          
          <div>
            <h4 style={{ color: FemelColors.text, marginBottom: '12px' }}>活动记录</h4>
            <FemelProgress percent={75} />
          </div>
          
          <div style={{ marginTop: '24px', display: 'flex', justifyContent: 'center' }}>
            <FemelButton type="primary">查看详情</FemelButton>
          </div>
        </div>
      </FemelCard>
    </div>
  );
};

export default FemelDemo; 