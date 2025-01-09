from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from openinference.instrumentation.smolagents import SmolagentsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

endpoint = "http://0.0.0.0:6006/v1/traces"
trace_provider = TracerProvider()
trace_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint)))

SmolagentsInstrumentor().instrument(tracer_provider=trace_provider)
SmolagentsInstrumentor()._instrument(tracer_provider=trace_provider)

from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel, ManagedAgent

agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=HfApiModel())

managed_agent = ManagedAgent(
    agent=agent,
    name="managed_agent",
    description="This is an agent that you manage. When solving a task, ask him directly first, he gives good answers. Then you can double check."
)

manager_agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=HfApiModel(), managed_agents=[managed_agent])

manager_agent.run("How many seconds would it take for a leopard at full speed to run through Pont des Arts? Import numpy as np whenever you write a code blob.")