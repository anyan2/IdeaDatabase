import openai
from typing import List, Dict, Optional
import threading
import time
import json
import os
from datetime import datetime
openai.api_base = "http://127.0.0.1:1234/v1"
class AIProcessor:
    def __init__(self, db_handler, openai_api_key: str = ""):
        self.db_handler = db_handler
        self.openai_api_key = openai_api_key
        self.is_processing = False
        self.scheduled_task = None
        self.memory_file = "data/ai_memory.json"
        self.model="gpt-3.5-turbo"
        
        # 确保数据目录存在
        os.makedirs('data', exist_ok=True)
        
        # 初始化AI记忆
        if not os.path.exists(self.memory_file):
            self.save_memory({
                "last_processed": None,
                "meta_summary": "",
                "insights": [],
                "reminders": []
            })
    def update_config(self,api_key=None,model=None):
        #更新配置信息，于ui中调用并刷新
        if api_key is not None:
            self.openai_api_key=api_key
        if model is not None:
            self.model = model
    def process_ideas(self):
        """处理所有想法，生成标签、摘要和关联"""
        if not self.openai_api_key:
            print("OpenAI API密钥未设置，跳过AI处理")
            return
        
        if self.is_processing:
            print("AI处理器已经在运行中")
            return
            
        self.is_processing = True
        try:
            openai.api_key = self.openai_api_key
            ideas = self.db_handler.get_all_ideas()
            
            # 为没有标签的想法生成标签
            for idea in ideas:
                if not idea.get('tags'):
                    tags = self.generate_tags(idea['content'])
                    if tags:
                        self.db_handler.update_idea_tags(idea['id'], tags)
                
                if not idea.get('summary'):
                    summary = self.generate_summary(idea['content'])
                    if summary:
                        self.db_handler.update_idea_summary(idea['id'], summary)
            
            # 生成整体摘要和见解
            self.generate_insights(ideas)
            
            # 更新AI记忆
            memory = self.load_memory()
            memory["last_processed"] = datetime.now().isoformat()
            self.save_memory(memory)
            
        except Exception as e:
            print(f"AI处理出错: {e}")
        finally:
            self.is_processing = False

    def generate_tags(self, idea: str) -> List[str]:
        """
        生成想法的标签
        
        Args:
            idea: 想法内容
            
        Returns:
            标签列表
        """
        try:
            # 使用OpenAI API生成标签
            response = openai.ChatCompletion.create(
                #model="gpt-3.5-turbo",
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个标签生成助手。请为下面的内容生成3-5个关键标签，每个标签应该是单个词或短语，能够概括内容的主题或要点。返回格式应为JSON数组。"},
                    {"role": "user", "content": idea}
                ],
                max_tokens=100,
                temperature=0.3
            )
            
            # 解析回复
            content = response.choices[0].message.content.strip()
            # 尝试直接解析JSON
            try:
                tags = json.loads(content)
                if isinstance(tags, list):
                    return tags
            except:
                pass
                
            # 如果不是直接的JSON，尝试找到JSON数组的部分
            import re
            match = re.search(r'\[(.*?)\]', content.replace('\n', ' '), re.DOTALL)
            if match:
                try:
                    tags = json.loads(f"[{match.group(1)}]")
                    return tags
                except:
                    pass
            
            # 最后的备选方案，按逗号分割
            if ',' in content:
                return [tag.strip().strip('"\'') for tag in content.split(',')]
                
            # 如果都失败了，返回单个标签
            return [content.strip().strip('"\'')]
            
        except Exception as e:
            print(f"生成标签时出错: {e}")
            return []

    def generate_summary(self, idea: str) -> str:
        """
        生成想法的摘要
        
        Args:
            idea: 想法内容
            
        Returns:
            摘要内容
        """
        try:
            # 使用OpenAI API生成摘要
            response = openai.ChatCompletion.create(
                #model="gpt-3.5-turbo",
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个摘要生成助手。请为下面的内容生成一个简短的摘要，不超过30个字。"},
                    {"role": "user", "content": idea}
                ],
                max_tokens=60,
                temperature=0.3
            )
            
            # 返回摘要
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"生成摘要时出错: {e}")
            return ""

    def generate_insights(self, ideas: List[Dict]):
        """
        根据所有想法生成整体见解和提醒
        
        Args:
            ideas: 想法列表
        """
        if not ideas:
            return
            
        try:
            # 准备输入数据
            idea_summaries = []
            for idea in ideas:
                timestamp = datetime.fromisoformat(idea['timestamp']).strftime("%Y-%m-%d %H:%M")
                tags = ", ".join(idea['tags']) if idea['tags'] else "无标签"
                summary = idea['summary'] if idea['summary'] else "无摘要"
                idea_summaries.append(f"ID: {idea['id']}, 时间: {timestamp}, 标签: [{tags}], 摘要: {summary}")
            
            # 限制输入长度，防止超出token限制
            idea_input = "\n".join(idea_summaries[-50:])  # 只使用最近的50条想法
            
            # 加载现有记忆
            memory = self.load_memory()
            
            # 使用OpenAI API生成见解
            response = openai.ChatCompletion.create(
                #model="gpt-3.5-turbo-16k",
                model=self.model,
                messages=[
                    {"role": "system", "content": f"""你是一个智能想法分析助手。
请根据用户的想法历史，生成有价值的见解和建议。这些见解应该能帮助用户发现隐藏的模式、主题和机会。
你应当分析最近的想法趋势，识别重要主题，并提供相关的建议和提醒。

过去的见解摘要: {memory.get('meta_summary', '无')}

请返回JSON格式的回复，包含以下字段:
1. meta_summary: 对用户所有想法的元级总结
2. insights: 一个包含3-5条新见解的数组，每条见解应当有title和content字段
3. reminders: 一个包含1-3条提醒的数组，指出用户应该在何时回顾或行动的事项，每条提醒包含content和due_date字段
"""},
                    {"role": "user", "content": f"这是我最近的想法摘要:\n{idea_input}"}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            # 解析回复
            content = response.choices[0].message.content.strip()
            
            try:
                # 尝试解析JSON
                result = json.loads(content)
                
                # 更新记忆
                if "meta_summary" in result:
                    memory["meta_summary"] = result["meta_summary"]
                
                if "insights" in result and isinstance(result["insights"], list):
                    # 添加时间戳到每个见解
                    for insight in result["insights"]:
                        insight["timestamp"] = datetime.now().isoformat()
                    
                    # 合并见解，保留最近的10条
                    memory["insights"] = result["insights"] + memory.get("insights", [])
                    memory["insights"] = memory["insights"][:10]
                
                if "reminders" in result and isinstance(result["reminders"], list):
                    # 处理提醒
                    new_reminders = []
                    for reminder in result["reminders"]:
                        # 确保reminder有必要的字段
                        if isinstance(reminder, dict) and "content" in reminder:
                            # 如果没有due_date，默认为一周后
                            if "due_date" not in reminder:
                                future = datetime.now()
                                future = future.replace(day=future.day + 7)
                                reminder["due_date"] = future.strftime("%Y-%m-%d")
                            new_reminders.append(reminder)
                    
                    # 合并提醒，保留所有未到期的提醒
                    today = datetime.now().strftime("%Y-%m-%d")
                    old_reminders = [r for r in memory.get("reminders", []) 
                                    if r.get("due_date", "2000-01-01") >= today]
                    
                    memory["reminders"] = new_reminders + old_reminders
                
                # 保存更新后的记忆
                self.save_memory(memory)
                
            except Exception as e:
                print(f"解析AI见解时出错: {e}")
                print(f"原始回复: {content}")
            
        except Exception as e:
            print(f"生成见解时出错: {e}")

    def query_ai(self, query: str) -> str:
        """
        向AI提问，关于用户的想法和见解
        
        Args:
            query: 用户的问题
            
        Returns:
            AI的回答
        """
        if not self.openai_api_key:
            return "OpenAI API密钥未设置，无法处理查询。"
        
        try:
            openai.api_key = self.openai_api_key
            
            # 获取记忆
            memory = self.load_memory()
            
            # 准备上下文
            context = f"""元级总结: {memory.get('meta_summary', '无总结')}

最近的见解:
"""
            
            for i, insight in enumerate(memory.get("insights", [])[:5]):
                context += f"{i+1}. {insight.get('title', '无标题')}: {insight.get('content', '无内容')}\n"
            
            context += "\n即将到来的提醒:\n"
            
            today = datetime.now().strftime("%Y-%m-%d")
            upcoming_reminders = [r for r in memory.get("reminders", []) 
                                if r.get("due_date", "2000-01-01") >= today]
            
            for i, reminder in enumerate(upcoming_reminders[:3]):
                context += f"{i+1}. {reminder.get('due_date', '无日期')}: {reminder.get('content', '无内容')}\n"
            
            # 查询AI
            response = openai.ChatCompletion.create(
                #model="gpt-3.5-turbo",
                model=self.model,
                messages=[
                    {"role": "system", "content": f"""你是一个智能想法分析助手。
你有关于用户想法历史的上下文知识，并且你的任务是回答用户关于他们想法的问题。
基于以下上下文，以友好、有帮助的方式回答用户的问题。如果问题超出了你的上下文知识范围，请诚实说明。

上下文信息:
{context}"""},
                    {"role": "user", "content": query}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"查询AI时出错: {e}")
            return f"处理查询时出错: {str(e)}"

    def schedule_ai_task(self, interval: int):
        """
        设置定时任务，定期处理想法
        
        Args:
            interval: 定时任务的时间间隔，单位为秒
        """
        def scheduled_job():
            while True:
                self.process_ideas()
                time.sleep(interval)
        
        if self.scheduled_task is None or not self.scheduled_task.is_alive():
            self.scheduled_task = threading.Thread(target=scheduled_job, daemon=True)
            self.scheduled_task.start()
    
    def load_memory(self) -> Dict:
        """加载AI记忆"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载AI记忆时出错: {e}")
        
        # 如果文件不存在或读取出错，返回空记忆
        return {
            "last_processed": None,
            "meta_summary": "",
            "insights": [],
            "reminders": []
        }
    
    def save_memory(self, memory: Dict):
        """保存AI记忆"""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(memory, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存AI记忆时出错: {e}")
    
    def get_upcoming_reminders(self) -> List[Dict]:
        """获取即将到来的提醒"""
        memory = self.load_memory()
        today = datetime.now().strftime("%Y-%m-%d")
        return [r for r in memory.get("reminders", []) 
                if r.get("due_date", "2000-01-01") >= today]
    
    def get_insights(self) -> List[Dict]:
        """获取见解列表"""
        memory = self.load_memory()
        return memory.get("insights", [])